<template>
	<div class="CoreSliderInput" ref="rootEl">
		<label>{{ fields.label }}</label>
		<div class="inputArea">
			<input
				type="range"
				v-model="formValue"
				:min="fields.minValue"
				:max="fields.maxValue"
				:step="fields.stepSize"
			/>
			<div class="valueContainer">
				<h3>{{ formValue }}</h3>
			</div>
		</div>
	</div>
</template>

<script lang="ts">
import { FieldType } from "../streamsyncTypes";

export default {
	streamsync: {
		name: "Slider Input",
		description: "Allows the user to input numeric values using a slider.",
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
				type: FieldType.Number,
				default: "0",
				init: "0",
			},
			minValue: {
				name: "Minimum value",
				type: FieldType.Number,
				default: "0",
				init: "0",
			},
			maxValue: {
				name: "Maximum value",
				type: FieldType.Number,
				default: "100",
				init: "100",
			},
			stepSize: {
				name: "Step size",
				type: FieldType.Number,
				default: "1",
				init: "1",
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

.CoreSliderInput {
	width: 100%;
	max-width: 40ch;
}

label {
	display: block;
	margin-bottom: 8px;
	color: var(--primaryTextColor);
}

.inputArea {
	display: flex;
}

input {
	flex: 1 0 auto;
	margin: 0;
}

.valueContainer {
	margin-left: 8px;
	flex: 0 0 auto;
	text-align: right;
}
</style>
