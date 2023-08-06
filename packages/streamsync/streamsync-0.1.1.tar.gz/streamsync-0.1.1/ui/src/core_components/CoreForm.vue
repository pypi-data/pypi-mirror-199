<template>
	<div class="CoreForm" ref="rootEl">
		<div data-streamsync-container><slot></slot></div>
		<div class="actions">
			<button
				v-on:click="submit"
				:disabled="isSubmitting ? true : undefined"
			>
				{{ fields.submitDesc }}
			</button>
			<div class="submitting" v-if="isSubmitting">Submitting...</div>
			<div
				class="result"
				v-if="submissionResult"
				:class="{ ok: submissionResult?.ok }"
			>
				<div class="message">
					<template v-if="submissionResult.message">
						{{ submissionResult.message }}
					</template>
					<template v-else>
						<template v-if="!submissionResult.ok">
							Invalid values provided.
						</template>
					</template>
				</div>
			</div>
		</div>
	</div>
</template>

<script lang="ts">
import { Component, FieldType } from "../streamsyncTypes";
import {
	buttonColor,
	buttonTextColor,
	buttonShadow,
	separatorColor,
} from "../renderer/sharedStyleFields";

const ssSubmitStub = `
def form_submit_handler(state, payload):

	# When submitting a form, values from all of its Input
	# descendents are gathered into a dictionary. The keys for the dictionary
	# are the "Key" field of each Input component.

	# For example, if you have a Form with a Text Input (Key: name) and a
	# Radio Input (Key: fav_animal) you'll get a dictionary like
	# {"name": "Veronica", "fav_animal": "monkey"}.

    name = payload.get("name")
    fav_animal = payload.get("fav_animal")
    state["message"] = f"{name} said that their favourite animal is {fav_animal}."

	# If a File Input is added (Key: files), an array of dictionaries is provided
	# The dictionaries have the properties name, type and data
    # The data property is a file-like object

    uploaded_files = payload.get("files")
    for i, uploaded_file in enumerate(uploaded_files):
        file_data = uploaded_file.get("data")
        with open(f"{name}-{i}.jpeg", "wb") as file_handle:
            file_handle.write(file_data)`.trim();

export default {
	streamsync: {
		name: "Form",
		description: "A form.",
		category: "Input",
		allowedChildrenTypes: ["*"],
		fields: {
			submitDesc: {
				name: "Submit Button Description",
				default: "(No description)",
				init: "Submit",
				type: FieldType.Text,
			},
			clearFormAfterSubmission: {
				name: "Clear form after submission",
				init: "yes",
				desc: "Whether to clear the form after successful submissions.",
				type: FieldType.Text,
				default: "yes",
				options: {
					yes: "Yes",
					no: "No",
				},
			},
			buttonColor,
			buttonTextColor,
			buttonShadow,
			separatorColor,
		},
		events: {
			"ss-submit": {
				desc: "Submit the form.",
				stub: ssSubmitStub,
			},
		},
	},
};
</script>

<script setup lang="ts">
import { inject, ref, Ref } from "vue";
import injectionKeys from "../injectionKeys";

const fields = inject(injectionKeys.evaluatedFields);
const ss = inject(injectionKeys.core);
const componentId = inject(injectionKeys.componentId);
const rootEl: Ref<HTMLElement> = ref(null);
const isSubmitting = ref(false);

type SubmissionResult = {
	ok: boolean;
	message?: string;
};

const submissionResult: Ref<SubmissionResult> = ref(null);

const getProcessedChildrenFormValues = async (parentId: Component["id"]) => {
	const processedFormValues = {};
	const childrenComponents = ss.getComponents(parentId);

	for (let i = 0; i < childrenComponents.length; i++) {
		const child = childrenComponents[i];
		const processedChildFormValues = await getProcessedChildrenFormValues(
			child.id
		);
		Object.assign(processedFormValues, processedChildFormValues);

		const formValue = ss.getFormValue(child.id);
		if (typeof formValue == "undefined") continue;

		let processedFormValue: any;
		if (typeof formValue == "function") {
			processedFormValue = await formValue();
		} else {
			processedFormValue = formValue;
		}

		const key = child.content.key ?? child.id;
		processedFormValues[key] = processedFormValue;
	}
	return processedFormValues;
};

const clearChildrenFormValues = (parentId: Component["id"]) => {
	if (fields.value.clearFormAfterSubmission === "no") {
		return;
	}
	const childrenComponents = ss.getComponents(parentId);

	for (let i = 0; i < childrenComponents.length; i++) {
		const child = childrenComponents[i];
		clearChildrenFormValues(child.id);

		const formValue = ss.getFormValue(child.id);
		if (typeof formValue == "undefined") continue;
		ss.setFormValue(child.id, undefined);
	}
};

const submit = async () => {
	const component = ss.getComponentById(componentId);
	const isSubmitHandled =
		typeof component.handlers["ss-submit"] !== "undefined";
	if (!isSubmitHandled) return;

	isSubmitting.value = true;
	submissionResult.value = null;

	let processedFormValues: Record<string, any>;
	try {
		processedFormValues = await getProcessedChildrenFormValues(componentId);
	} catch (e) {
		isSubmitting.value = false;
		submissionResult.value = { ok: false, message: e.toString() };
		return;
	}
	const callback = ({ ok, payload }) => {
		isSubmitting.value = false;
		if (!ok || !payload.ok) {
			const message = !ok
				? "Couldn't connect."
				: "Form submission event failed.";
			submissionResult.value = { ok: false, message };
			return;
		}
		if (!payload.result) {
			clearChildrenFormValues(componentId);
			submissionResult.value = { ok: true, message: undefined };
			return;
		}
		if (payload.result.ok) {
			clearChildrenFormValues(componentId);
		}
		submissionResult.value = {
			ok: payload.result.ok,
			message: payload.result.message,
		};
	};
	const event = new CustomEvent("ss-submit", {
		detail: {
			payload: processedFormValues,
			callback,
		},
	});
	rootEl.value.dispatchEvent(event);
};
</script>

<style scoped>
@import "../renderer/sharedStyles.css";

.actions {
	margin-top: 16px;
	display: flex;
	align-items: center;
	gap: 16px;
}

.submitting {
	color: var(--secondaryTextColor);
}

.result {
	min-height: 100%;
}

.result:not(.ok) {
	color: red;
}
</style>
