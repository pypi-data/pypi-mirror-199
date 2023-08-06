<template>
	<div class="CoreCheckboxInput" ref="rootEl">
		<label class="mainLabel">{{ fields.label }}</label>
		<div class="options">
			<div
				class="option"
				v-for="(option, optionKey) in fields.options"
				:key="optionKey"
			>
				<input
					type="checkbox"
					v-model="formValue"
					:value="optionKey"
				/><label :for="`${flattenedInstancePath}-option-${optionKey}`">
					{{ option }}
				</label>
			</div>
		</div>
	</div>
</template>

<script lang="ts">
import { computed, inject, Ref, watch } from "vue";
import { ref } from "vue";
import { FieldType } from "../streamsyncTypes";

const defaultOptions = { a: "Option A", b: "Option B" };

const onChangeHandlerStub = `
def onchange_handler(state, payload):

	# Set the state variable "selected" to the selected options.
	# The payload will be a list, as multiple options are allowed.

	state["selected"] = payload`;

export default {
	streamsync: {
		name: "Checkbox Input",
		description:
			"Allows the user to choose a set of values using checkboxes.",
		category: "Input",
		fields: {
			label: {
				name: "Label",
				init: "Input Label",
				type: FieldType.Text,
			},
			key: {
				name: "Key",
				type: FieldType.Text,
				desc: "Used to identify the value during form submission.",
			},
			options: {
				name: "Options",
				control: "object",
				desc: "Key-value object with options. Must be a JSON string or a state reference to a dictionary.",
				type: FieldType.KeyValue,
				default: JSON.stringify(defaultOptions, null, 2),
			},
			initialValue: {
				name: "Initial value",
				type: FieldType.Object,
				default: "[]",
				desc: "Array containing the keys for the checked options.",
			},
		},
		events: {
			"ss-options-change": {
				desc: "Sent when the selected options change.",
				stub: onChangeHandlerStub.trim(),
			},
		},
	},
};
</script>

<script setup lang="ts">
import injectionKeys from "../injectionKeys";

const formValue = inject(injectionKeys.formValue);
const fields = inject(injectionKeys.evaluatedFields);
const instancePath = inject(injectionKeys.instancePath);
const rootEl: Ref<HTMLElement> = ref(null);

formValue.value = fields.value.initialValue;

watch(formValue, (newValue) => {
	if (typeof newValue === "undefined") {
		formValue.value = fields.value.initialValue;
	}
	const event = new CustomEvent("ss-options-change", {
		detail: { payload: formValue.value },
	});
	rootEl.value.dispatchEvent(event);
});

const flattenedInstancePath = computed(() => {
	const flat = instancePath
		.map((item) => `${item.componentId}:${item.instanceNumber}`)
		.join(".");
	return flat;
});
</script>

<style scoped>
@import "../renderer/sharedStyles.css";
.CoreCheckboxInput {
	width: 100%;
}

.options {
	display: flex;
	flex-direction: column;
	margin-top: 4px;
}

.option {
	margin-top: 8px;
	display: flex;
	align-items: center;
	color: var(--primaryTextColor);
	font-size: 0.75rem;
}

input {
	margin: 0 8px 0 0;
}

label {
	color: var(--primaryTextColor);
}
</style>
