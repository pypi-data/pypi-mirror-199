<template>
	<div class="CoreSeparator separator">
		<div class="line"></div>
	</div>
</template>

<script lang="ts">
import { separatorColor } from "../renderer/sharedStyleFields";

const description = `Visually separates elements.`;

const docs = `
Like Streamlit, but fast. A proof-of-concept framework built using JavaScript/Vue.js + Python/Flask + WebSockets.

By avoiding a rerun of the whole script, Streamsync can react more than 70 times faster. This is all achieved while 
maintaining a similar syntax. This repository is a companion to the following Medium article (no paywall),
which explains how Streamsync was built, the tests conducted and the implications.
`;

export default {
	streamsync: {
		name: "Separator",
		description,
		docs,
		category: "Layout",
		fields: {
			separatorColor,
		},
	},
};
</script>

<style scoped>
@import "../renderer/sharedStyles.css";
.CoreSeparator {
	min-height: 1px;
	min-width: 1px;
	align-self: stretch;
	margin: -4px;
	padding: 4px;
}

.line {
	background-color: var(--separatorColor);
	width: 100%;
	height: 100%;
	min-height: 1px;
	min-width: 1px;
}
</style>
