<template>
	<div class="CoreSection" :class="{ snapMode: fields.snapMode == 'yes' }">
		<h2 v-if="fields.title">{{ fields.title }}</h2>
		<div data-streamsync-container><slot></slot></div>
	</div>
</template>

<script lang="ts">
import { FieldCategory, FieldType } from "../streamsyncTypes";
import * as sharedStyleFields from "../renderer/sharedStyleFields";

const description = `Standard container with an optional title.`;

const docs = `
Like Streamlit, but fast. A proof-of-concept framework built using JavaScript/Vue.js + Python/Flask + WebSockets.

By avoiding a rerun of the whole script, Streamsync can react more than 70 times faster. This is all achieved while 
maintaining a similar syntax. This repository is a companion to the following Medium article (no paywall),
which explains how Streamsync was built, the tests conducted and the implications.
`;

export default {
	streamsync: {
		name: "Section",
		description,
		docs,
		category: "Layout",
		allowedChildrenTypes: ["*"],
		fields: {
			title: {
				name: "Title",
				init: "Section Title",
				desc: "Leave blank to hide.",
				type: FieldType.Text,
			},
			...sharedStyleFields,
			snapMode: {
				name: "Snap mode",
				type: FieldType.Text,
				options: {
					no: "No",
					yes: "Yes",
				},
				default: "no",
				init: "no",
				category: FieldCategory.Style,
				desc: "Use as much space as possible without altering the size of the container.",
			},
		},
		previewField: "title",
	},
};
</script>
<script setup lang="ts">
import { inject } from "vue";
import injectionKeys from "../injectionKeys";

const fields = inject(injectionKeys.evaluatedFields);
</script>

<style scoped>
@import "../renderer/sharedStyles.css";
.CoreSection {
	padding: 16px;
	border: 1px solid var(--separatorColor);
	border-radius: 8px;
	box-shadow: var(--containerShadow);
	background-color: var(--containerBackgroundColor);
}

.CoreSection.snapMode {
	flex: 1 0 auto;
	align-self: stretch;
}

h2 {
	margin-bottom: 16px;
}
</style>
