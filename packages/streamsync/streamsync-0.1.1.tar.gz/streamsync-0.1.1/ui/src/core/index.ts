import { ref, Ref } from "vue";
import {
	Component,
	ComponentMap,
	InstancePath,
	MailItem,
} from "../streamsyncTypes";
import {
	getSupportedComponentTypes,
	getComponentDefinition,
} from "./templateMap";
import * as typeHierarchy from "./typeHierarchy";

const RECONNECT_DELAY_MS = 1000;

export function generateCore() {
	let sessionId: string = null;
	let mode: Ref<"run" | "edit"> = ref(null);
	let savedCode: Ref<string> = ref(null);
	let runCode: Ref<string> = ref(null);
	const isCallbackPending: Ref<boolean> = ref(false);
	const components: Ref<ComponentMap> = ref({});
	const userFunctions: Ref<string[]> = ref([]);
	const userState: Ref<Record<string, any>> = ref({});
	const formValues: Ref<Record<Component["id"], any>> = ref({});
	let webSocket: WebSocket;
	const syncHealth: Ref<"idle" | "connected" | "offline"> = ref("idle");
	let frontendMessageCounter = 0;
	const frontendMessageCallbackMap: Map<number, Function> = new Map();
	let mailInbox: MailItem[] = [];
	const mailSubscriptions: { mailType: string; fn: Function }[] = [];
	let activePageId: Ref<Component["id"]> = ref(null);

	/**
	 * Whether Streamsync is running as builder or runner.
	 * The mode is enforced in the backend and used in the frontend for presentation purposes only.
	 *
	 * @returns
	 */
	function getMode() {
		return mode.value;
	}

	/**
	 * Initialise the core.
	 * @returns
	 */
	async function init() {
		await initSession();
		addMailSubscription("pageChange", (pageKey: string) => {
			setActivePageFromKey(pageKey);
		});

		if (mode.value != "edit") return;
	}

	/**
	 * Initialise a session by loading a starter pack from the backend.
	 *
	 * @returns
	 */
	async function initSession() {
		const response = await fetch("/api/init", { cache: "no-store" });
		const initData = await response.json();

		mode.value = initData.mode;
		components.value = initData.components;
		userState.value = initData.userState;
		collateMail(initData.mail);
		sessionId = initData.sessionId;

		// Only returned for edit (Builder) mode

		userFunctions.value = initData.userFunctions;
		savedCode.value = initData.savedCode;
		runCode.value = initData.runCode;
		await startSync();
	}

	async function reinitSession() {
		frontendMessageCallbackMap.forEach((callback) => {
			callback({ ok: false });
		});
		frontendMessageCallbackMap.clear();
		isCallbackPending.value = false;
		await initSession();
	}

	function ingestMutations(mutations: Record<string, any>) {
		Object.entries(mutations).forEach(([key, value]) => {
			const accessor = key.split(".");
			let stateRef = userState.value;
			for (let i = 0; i < accessor.length - 1; i++) {
				stateRef = stateRef[accessor[i]];
			}
			stateRef[accessor.at(-1)] = value;
		});
	}

	// Open and setup websocket

	async function startSync(): Promise<void> {
		if (webSocket) return; // Open WebSocket exists

		const url = new URL("/api/stream", window.location.href);
		url.protocol = url.protocol.replace("https", "wss");
		url.protocol = url.protocol.replace("http", "ws");
		webSocket = new WebSocket(url.href);

		webSocket.onopen = () => {
			syncHealth.value = "connected";
			console.log("WebSocket connected. Initialising stream...");
			sendFrontendMessage("streamInit", { sessionId });
		};

		webSocket.onmessage = (wsEvent) => {
			const message = JSON.parse(wsEvent.data);
			const { mutations, mail } = message;

			if (mutations) ingestMutations(mutations);
			collateMail(mail);

			if (
				message.messageType == "announcement" &&
				message.payload.announce == "codeUpdate"
			) {
				webSocket.close();
				reinitSession();
				return;
			}

			// Handle callback

			const callback: Function = frontendMessageCallbackMap.get(
				message.trackingId
			);

			if (typeof callback === "undefined") return;
			frontendMessageCallbackMap.delete(message.trackingId);
			callback({ ok: true, payload: message.payload });
			if (frontendMessageCallbackMap.size == 0) {
				isCallbackPending.value = false;
			}
		};

		webSocket.onclose = async (ev: CloseEvent) => {
			webSocket = null;
			syncHealth.value = "offline";

			if (ev.code == 1008) {
				// 1008: Policy Violation
				// Connection established correctly but closed due to invalid session.
				// Do not attempt to reconnect, the session will remain invalid. Initialise a new session.

				console.error("Invalid session. Reinitialising...");

				// Take care of pending event resolutions and fail them.
				await reinitSession();
				return;
			}

			// Connection lost due to some other reason. Try to reconnect.

			console.error("WebSocket closed. Attempting to reconnect...");
			setTimeout(async () => {
				try {
					await startSync();
				} catch {
					console.error("Couldn't reconnect.");
				}
			}, RECONNECT_DELAY_MS);
		};

		return new Promise((resolve, reject) => {
			webSocket.addEventListener("open", () => resolve(), { once: true });
			webSocket.addEventListener("close", () => reject(), { once: true });
		});
	}

	/**
	 * Dispatches the given mail to the relevant mail subscriptions.
	 * Items that cannot be distributed remain in the inbox.
	 *
	 * @param mail
	 * @returns
	 */
	function collateMail(mail: MailItem[] = []) {
		mailInbox.push(...mail);
		mailInbox = mailInbox.filter((item) => {
			const relevantSubscriptions = mailSubscriptions.filter(
				(ms) => ms.mailType == item.type
			);

			if (relevantSubscriptions.length == 0) {
				return item;
			}

			relevantSubscriptions.forEach((ms) => ms.fn(item.payload));
		});
	}

	function addMailSubscription(mailType: string, fn: Function) {
		mailSubscriptions.push({ mailType, fn });
		collateMail();
	}

	function forwardEvent(event: Event, instancePath: InstancePath) {
		let eventPayload = null;
		let callback: Function;
		if (event instanceof CustomEvent) {
			eventPayload = event.detail?.payload ?? null;
			callback = event.detail?.callback;
		}

		if (!callback) {
			callback = () => null;
		}

		const messagePayload = {
			type: event.type,
			instancePath,
			payload: eventPayload,
		};

		sendFrontendMessage("event", messagePayload, callback);
	}

	async function sendCodeSaveRequest(newCode: string): Promise<void> {
		const messageData = {
			code: newCode,
		};

		return new Promise((resolve, reject) => {
			const messageCallback = (r: {
				ok: boolean;
				payload?: Record<string, any>;
			}) => {
				if (!r.ok) {
					reject("Couldn't connect to the server.");
					return;
				}
				resolve();
			};

			sendFrontendMessage(
				"codeSaveRequest",
				messageData,
				messageCallback
			);
		});
	}

	function getSavedCode() {
		return savedCode.value;
	}

	async function sendCodeUpdate(newCode: string): Promise<void> {
		const messageData = {
			code: newCode,
		};

		return new Promise((resolve, reject) => {
			const messageCallback = (r: {
				ok: boolean;
				payload?: Record<string, any>;
			}) => {
				if (!r.ok) {
					reject("Couldn't connect to the server.");
					return;
				}
				resolve();
			};
			sendFrontendMessage("codeUpdate", messageData, messageCallback);
		});
	}

	function getRunCode() {
		return runCode.value;
	}

	function sendFrontendMessage(
		type: string,
		payload: object,
		callback?: Function
	) {
		const trackingId = frontendMessageCounter++;
		try {
			const wsData = {
				type,
				trackingId,
				payload,
			};
			if (webSocket.readyState !== webSocket.OPEN) {
				throw "Connection lost.";
			}
			webSocket.send(JSON.stringify(wsData));
			if (!callback) return;
			isCallbackPending.value = true;
			frontendMessageCallbackMap.set(trackingId, callback);
		} catch {
			if (!callback) return;
			callback({ ok: false });
		}
	}

	function deleteComponent(componentId: Component["id"]) {
		// delete renderedComponents[componentId];
		delete components.value[componentId];
	}

	function addComponent(component: Component) {
		components.value[component.id] = component;
	}

	/**
	 * Triggers a component update.
	 * @returns
	 */
	async function sendComponentUpdate(): Promise<void> {
		const payload = {
			components: components.value,
		};

		return new Promise((resolve, reject) => {
			const messageCallback = (r: {
				ok: boolean;
				payload?: Record<string, any>;
			}) => {
				if (!r.ok) {
					reject("Couldn't connect to the server.");
					return;
				}
				resolve();
			};
			sendFrontendMessage("componentUpdate", payload, messageCallback);
		});
	}

	function getUserFunctions() {
		return userFunctions.value;
	}

	function getFormValue(componentId: Component["id"]) {
		return formValues.value[componentId];
	}

	function setFormValue(componentId: Component["id"], value: any) {
		formValues.value[componentId] = value;
	}

	function getComponentById(componentId: Component["id"]): Component {
		return components.value[componentId];
	}

	/**
	 * Check the visibility of a component.
	 *
	 * @param componentId The id of the component.
	 * @param fullTree Whether to check the component and all its ancestors or just the component.
	 * @returns Visibility status.
	 */
	function isComponentVisible(
		componentId: Component["id"],
		fullTree = false
	): boolean {
		const component = components.value[componentId];
		if (!component) return false;

		if (
			fullTree &&
			component.parentId &&
			!isComponentVisible(component.parentId)
		) {
			return false;
		}

		if (component.visible === true) return true;
		if (component.visible === false) return false;
		const evaluated = evaluateExpression(component.visible as string);
		return !!evaluated;
	}

	/**
	 * Gets registered Streamsync components.
	 *
	 * @param childrenOfId If specified, only include results that are children of a component with this id.
	 * @param sortedByPosition Whether to sort the components by position or return in random order.
	 * @returns An array of components.
	 */
	function getComponents(
		childrenOfId: Component["id"] = undefined,
		sortedByPosition: boolean = false
	): Component[] {
		let ca = Object.values(components.value);

		if (typeof childrenOfId != "undefined") {
			ca = ca.filter((c) => c.parentId == childrenOfId);
		}
		if (sortedByPosition) {
			ca = ca.sort((a, b) => (a.position > b.position ? 1 : -1));
		}
		return ca;
	}

	function setActivePageFromKey(targetPageKey: string) {
		const pages = getComponents("root");
		const matches = pages.filter((pageComponent) => {
			const pageKey = pageComponent.content["key"];
			return pageKey == targetPageKey;
		});
		if (matches.length == 0) return;
		setActivePageId(matches[0].id);
	}

	function getPageKeys() {
		const pages = getComponents("root");
		const pageKeys = pages
			.map((page) => page.content["key"])
			.filter((pageKey) => !!pageKey);
		return pageKeys;
	}

	function setActivePageId(componentId: Component["id"]) {
		activePageId.value = componentId;
	}

	function getActivePageId(): Component["id"] {
		return activePageId.value;
	}

	function getContainableTypes(componentId: Component["id"]) {
		return typeHierarchy.getContainableTypes(components.value, componentId);
	}

	function evaluateExpression(
		expr: string,
		contextData?: Record<string, any>
	) {
		const splitKey = expr.split(".");
		let contextRef = contextData;
		let stateRef = userState.value;

		for (let i = 0; i < splitKey.length; i++) {
			contextRef = contextRef?.[splitKey[i]];
			stateRef = stateRef?.[splitKey[i]];
		}

		return contextRef ?? stateRef;
	}

	const core = {
		webSocket,
		syncHealth,
		isCallbackPending,
		getMode,
		getUserFunctions,
		addMailSubscription,
		init,
		evaluateExpression,
		isComponentVisible,
		forwardEvent,
		getSavedCode,
		getRunCode,
		sendCodeSaveRequest,
		sendCodeUpdate,
		sendComponentUpdate,
		addComponent,
		deleteComponent,
		getFormValue,
		setFormValue,
		getComponentById,
		getComponents,
		setActivePageId,
		getActivePageId,
		getPageKeys,
		setActivePageFromKey,
		getComponentDefinition,
		getSupportedComponentTypes,
		getContainableTypes,
	};

	return core;
}
