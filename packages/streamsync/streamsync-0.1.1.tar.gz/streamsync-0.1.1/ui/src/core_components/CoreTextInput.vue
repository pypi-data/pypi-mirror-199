<template>
	<div class="CoreTextInput" ref="rootEl">
		<label>{{ fields.label }}</label>
		<input
			type="text"
			v-model="formValue"
			:placeholder="fields.placeholder"
		/>
	</div>
</template>

<script lang="ts">
import { Component, FieldType } from "../streamsyncTypes";

export default {
	streamsync: {
		name: "Text Input",
		description: "Allows the user to input text values.",
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
			initialValue: {
				name: "Initial value",
				type: FieldType.Text,
				default: "",
			},
			placeholder: {
				name: "Placeholder",
				type: FieldType.Text,
			},
		},
		events: {
			"ss-change": {
				desc: "Capture changes to this control.",
			},
		},
	},
};
</script>

<script setup lang="ts">
import { inject, ref, watch } from "vue";
import injectionKeys from "../injectionKeys";

const formValue = inject(injectionKeys.formValue);
const fields = inject(injectionKeys.evaluatedFields);
const rootEl = ref(null);

formValue.value = fields.value.initialValue;

watch(formValue, (newValue) => {
	if (typeof newValue === "undefined") {
		formValue.value = fields.value.initialValue;
	}

	const event = new CustomEvent("ss-change", {
		detail: { payload: formValue.value },
	});
	rootEl.value.dispatchEvent(event);
});
</script>

<style scoped>
@import "../renderer/sharedStyles.css";

.CoreTextInput {
	max-width: 70ch;
	width: 100%;
}

label {
	display: block;
	margin-bottom: 8px;
	color: var(--primaryTextColor);
}

input {
	margin: 0;
	border: 1px solid var(--separatorColor);
}
</style>
