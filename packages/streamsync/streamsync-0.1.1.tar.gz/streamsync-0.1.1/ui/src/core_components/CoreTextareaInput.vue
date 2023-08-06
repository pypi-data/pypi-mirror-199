<template>
	<div class="CoreTextareaInput" ref="rootEl">
		<label>{{ fields.label }}</label>
		<textarea
			v-model="formValue"
			:placeholder="fields.placeholder"
			:rows="fields.rows"
		></textarea>
	</div>
</template>

<script lang="ts">
import { FieldType } from "../streamsyncTypes";

export default {
	streamsync: {
		name: "Textarea Input",
		description: "Allows the user to input multiline text values.",
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
				control: "textarea",
			},
			rows: {
				name: "Rows",
				type: FieldType.Number,
				init: "5",
				default: "5",
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

.CoreTextareaInput {
	max-width: 70ch;
	width: 100%;
}

label {
	display: block;
	margin-bottom: 8px;
	color: var(--primaryTextColor);
}

textarea {
	width: 100%;
	margin: 0;
	border: 1px solid var(--separatorColor);
}
</style>
