<template>
	<div class="CoreDropdownInput" ref="rootEl">
		<label class="mainLabel">{{ fields.label }}</label>
		<div class="selectContainer">
			<select v-model="formValue">
				<option
					v-for="(option, optionKey) in fields.options"
					:key="optionKey"
					:value="optionKey"
				>
					{{ option }}
				</option>
			</select>
		</div>
	</div>
</template>

<script lang="ts">
import { inject, onMounted, Ref, watch } from "vue";
import { ref } from "vue";
import { FieldType } from "../streamsyncTypes";

const defaultOptions = { a: "Option A", b: "Option B" };

const onChangeHandlerStub = `
def onchange_handler(state, payload):

	# Set the state variable "selected" to the selected option

	state["selected"] = payload`;

export default {
	streamsync: {
		name: "Dropdown Input",
		description:
			"Allows the user to choose a value using a dropdown (also known as select) input.",
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
		},
		events: {
			"ss-option-change": {
				desc: "Sent when the selected option changes.",
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
const rootEl: Ref<HTMLElement> = ref(null);

formValue.value = fields.value.initialValue;

watch(formValue, (newValue) => {
	if (typeof newValue === "undefined") {
		formValue.value = fields.value.initialValue;
	}
	const event = new CustomEvent("ss-option-change", {
		detail: { payload: formValue.value },
	});
	rootEl.value.dispatchEvent(event);
});
</script>

<style scoped>
@import "../renderer/sharedStyles.css";
.CoreSelectInput {
	width: 100%;
}

label {
	color: var(--primaryTextColor);
}

.selectContainer {
	margin-top: 8px;
}
</style>
