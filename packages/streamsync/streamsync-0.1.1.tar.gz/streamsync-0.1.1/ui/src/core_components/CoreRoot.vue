<template>
	<div class="CoreRoot" data-streamsync-container ref="rootEl">
		<template v-for="vnode in getChildrenVNodes()">
			<component
				:is="vnode"
				v-if="vnode.key === `${activePageId}:0`"
			></component>
		</template>
	</div>
</template>

<script lang="ts">
import { FieldType } from "../streamsyncTypes";
import * as sharedStyleFields from "../renderer/sharedStyleFields";

const ssHashChangeStub = `
def handle_hashchange(state, payload):
	# The payload is a dictionary with the page key and all the route variables in the URL hash.
	# For example, if the current URL is
	# http://localhost:3000/#main/animal=duck&colour=yellow
	# you will get the following dictionary
	# {
	#	"page_key": "main",
	#	"route_vars": {
	#		"animal": "duck",
	#		"colour": "yellow"
	#	}
	# }

	page_key = payload.get("page_key")
	route_vars = payload.get("route_vars")

	if not route_vars:
		return

	if route_vars.get("animal") == "duck":
		state["message"] = "You've navigated to the Duck zone."
	else:
		state["message"] = "You're not in the Duck zone.`.trim();

export default {
	streamsync: {
		name: "Root",
		category: "Root",
		description: "Root component",
		allowedChildrenTypes: ["page"],
		fields: {
			appName: {
				name: "App name",
				type: FieldType.Text,
				desc: "The app name will be shown in the browser's title bar.",
			},
			...sharedStyleFields,
		},
		events: {
			"ss-hashchange": {
				desc: "Capture changes to hash variables.",
				stub: ssHashChangeStub,
			},
		},
	},
};
</script>
<script setup lang="ts">
import { computed, inject, onMounted, ref, Ref, watch } from "vue";
import injectionKeys from "../injectionKeys";

const ss = inject(injectionKeys.core);
const getChildrenVNodes = inject(injectionKeys.getChildrenVNodes);
const rootEl: Ref<HTMLElement> = ref(null);

const getFirstPageId = () => {
	const pageComponents = ss.getComponents("root", true);
	if (pageComponents.length == 0) return null;
	return pageComponents[0].id;
};

const hashRegex = /^((?<pageKey>[^\/]*))?(\/(?<routeVars>.*))?$/;
const routeVarRegex = /^(?<key>[^=]+)=(?<value>.*)$/;
const activePageId = computed(() => ss.getActivePageId() ?? getFirstPageId());

watch(
	activePageId,
	(newPageId) => {
		const page = ss.getComponentById(newPageId);
		const pageKey = page.content?.["key"];
		if (!pageKey) return;
		changePageInHash(pageKey);
	},
	{ immediate: true }
);

type ParsedHash = {
	pageKey?: string;
	routeVars: Record<string, string>;
};

function getParsedHash(): ParsedHash {
	const docHash = document.location.hash.substring(1);
	const hashMatchGroups = docHash.match(hashRegex)?.groups;
	let pageKey: string;
	let routeVars: Record<string, string> = {};

	if (!hashMatchGroups) return { pageKey, routeVars };
	pageKey = hashMatchGroups?.pageKey
		? decodeURIComponent(hashMatchGroups.pageKey)
		: undefined;
	const routeVarsSegments = hashMatchGroups.routeVars?.split("&") ?? [];

	routeVarsSegments.forEach((routeVarSegment) => {
		const matchGroups = routeVarSegment.match(routeVarRegex)?.groups;
		if (!matchGroups) return;
		const { key, value } = matchGroups;
		const decodedKey = decodeURIComponent(key);
		const decodedValue = decodeURIComponent(value);
		routeVars[decodedKey] = decodedValue;
	});

	return { pageKey, routeVars };
}

function setHash(parsedHash: ParsedHash) {
	const { pageKey, routeVars } = parsedHash;

	let hash = "";
	if (pageKey) {
		hash += `${encodeURIComponent(pageKey)}`;
	}
	if (Object.keys(routeVars).length > 0) {
		hash += "/";
		hash += Object.entries(routeVars)
			.map(([key, value]) => {
				// Vars set to null are excluded from the hash

				if (value === null) return null;
				return `${encodeURIComponent(key)}=${encodeURIComponent(
					value
				)}`;
			})
			.filter((segment) => segment)
			.join("&");
	}
	document.location.hash = hash;
}

function changePageInHash(targetPageKey: string) {
	const parsedHash = getParsedHash();
	parsedHash.pageKey = targetPageKey;
	setHash(parsedHash);
}

function changeRouteVarsInHash(targetRouteVars: Record<string, string>) {
	const parsedHash = getParsedHash();
	const routeVars = parsedHash?.routeVars ?? {};
	parsedHash.routeVars = { ...routeVars, ...targetRouteVars };
	setHash(parsedHash);
}

function handleHashChange() {
	const parsedHash = getParsedHash();
	const event = new CustomEvent("ss-hashchange", {
		detail: {
			payload: parsedHash,
		},
	});
	rootEl.value?.dispatchEvent(event);
	if (!parsedHash.pageKey) return;
	ss.setActivePageFromKey(parsedHash.pageKey);
}

onMounted(() => {
	ss.addMailSubscription("pageChange", (pageKey: string) => {
		changePageInHash(pageKey);
	});
	ss.addMailSubscription(
		"routeVarsChange",
		(routeVars: Record<string, string>) => {
			changeRouteVarsInHash(routeVars);
		}
	);
	window.addEventListener("hashchange", () => {
		handleHashChange();
	});
	handleHashChange();
});
</script>

<style scoped>
@import "../renderer/sharedStyles.css";

.CoreRoot {
	background: var(--emptinessColor);
	min-height: 100%;
	display: flex;
	width: 100%;
}

.CoreRoot.selected {
	background-color: var(--emptinessColor);
}
</style>
