<template>
	<div class="CoreText" :style="rootStyle">
		<template v-if="fields.useMarkdown == 'no'">
			<div class="plainText" :style="contentStyle">{{ fields.text }}</div>
		</template>
		<template v-else-if="fields.useMarkdown == 'yes'">
			<div
				class="markdown"
				:style="contentStyle"
				v-dompurify-html="unsanitisedMarkdownHtml"
			></div>
		</template>
	</div>
</template>

<script lang="ts">
import { FieldCategory, FieldType } from "../streamsyncTypes";
import { primaryTextColor } from "../renderer/sharedStyleFields";

const clickHandlerStub = `
def click_handler(state):

	# Increment counter when the text is clicked

	state["counter"] += 1`;

export default {
	streamsync: {
		name: "Text",
		description: "Displays plain or Markdown text.",
		category: "Content",
		fields: {
			text: {
				name: "Text",
				default: "(No text)",
				init: "Text",
				type: FieldType.Text,
				control: "textarea",
			},
			useMarkdown: {
				name: "Use Markdown",
				desc: "The Markdown output will be sanitised; unsafe elements will be removed.",
				default: "no",
				type: FieldType.Text,
				options: {
					yes: "Yes",
					no: "No",
				},
			},
			alignment: {
				name: "Alignment",
				default: "left",
				type: FieldType.Text,
				options: {
					left: "Left",
					center: "Center",
					right: "Right",
				},
				category: FieldCategory.Style,
			},
			primaryTextColor,
		},
		events: {
			click: {
				desc: "Capture single clicks.",
				stub: clickHandlerStub.trim(),
			},
		},
		previewField: "text",
	},
};
</script>
<script setup lang="ts">
import { marked } from "marked";
import { computed, inject } from "vue";
import injectionKeys from "../injectionKeys";

const fields = inject(injectionKeys.evaluatedFields);
const componentId = inject(injectionKeys.componentId);
const ss = inject(injectionKeys.core);

const rootStyle = computed(() => {
	const component = ss.getComponentById(componentId);
	const isClickHandled = typeof component.handlers["click"] !== "undefined";

	return {
		cursor: isClickHandled ? "pointer" : "unset",
	};
});

const contentStyle = computed(() => {
	return {
		"text-align": fields.value.alignment,
	};
});

const unsanitisedMarkdownHtml = computed(() => {
	const unsanitisedHtml = marked.parse(fields.value.text).trim();
	return unsanitisedHtml;
});
</script>

<style>
/*
WARNING: This style is non-scoped to allow rendered markdown to adopt
shared styles.
*/

@import "../renderer/sharedStyles.css";

.CoreText {
	color: var(--primaryTextColor);
	line-height: 1.5;
	white-space: pre-wrap;
}
</style>
