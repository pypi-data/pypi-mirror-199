<template>
	<div class="CoreButton">
		<button>
			{{ fields.text }}
		</button>
	</div>
</template>

<script lang="ts">
import {
	buttonColor,
	buttonTextColor,
	buttonShadow,
	separatorColor,
} from "../renderer/sharedStyleFields";

const clickHandlerStub = `
def handle_button_click(state):

	# Increment counter when the button is clicked

	state["counter"] += 1`;

export default {
	streamsync: {
		name: "Button",
		description:
			"A standalone button, which can be linked to a click event.",
		category: "Input",
		events: {
			click: {
				desc: "Capture single clicks.",
				stub: clickHandlerStub.trim(),
			},
		},
		fields: {
			text: {
				name: "Text",
				init: "Button Text",
				type: FieldType.Text,
			},
			buttonColor,
			buttonTextColor,
			buttonShadow,
			separatorColor,
		},
		previewField: "text",
	},
};
</script>
<script setup lang="ts">
import { inject } from "vue";
import { FieldType } from "../streamsyncTypes";
import injectionKeys from "../injectionKeys";

const fields = inject(injectionKeys.evaluatedFields);
</script>

<style scoped>
@import "../renderer/sharedStyles.css";
</style>
