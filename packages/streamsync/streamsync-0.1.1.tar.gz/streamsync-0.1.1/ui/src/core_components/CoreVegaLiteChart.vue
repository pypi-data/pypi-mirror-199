<template>
	<div class="CoreVegaLiteChart">
		<div ref="chartTargetEl"></div>
	</div>
</template>

<script lang="ts">
import { FieldType } from "../streamsyncTypes";

const description = `Standard container with an optional title.`;

const docs = `
Like Streamlit, but fast. A proof-of-concept framework built using JavaScript/Vue.js + Python/Flask + WebSockets.

# Summary

## By avoiding a rerun of the whole script, Streamsync can react more than 70 times faster. This is all achieved while
maintaining a similar syntax. This repository is a companion to the following Medium article (no paywall),
which explains how Streamsync was built, the tests conducted and the implications.
`;

const defaultSpec = {
	$schema: "https://vega.github.io/schema/vega-lite/v5.json",
	description:
		"Default chart. Use a JSON spec or pass a Vega Altair object via state.",
	data: {
		values: [
			{ a: "A", b: 100 },
			{ a: "B", b: 200 },
			{ a: "C", b: 150 },
			{ a: "D", b: 300 },
		],
	},
	mark: "bar",
	encoding: {
		x: { field: "a", type: "nominal" },
		y: { field: "b", type: "quantitative" },
	},
};

export default {
	streamsync: {
		name: "Vega Lite Chart",
		description,
		docs,
		category: "Content",
		fields: {
			spec: {
				name: "Chart definition",
				default: JSON.stringify(defaultSpec, null, 2),
				desc: "Vega-Lite chart specification. Pass a Vega Altair chart using state or paste a JSON specification.",
				type: FieldType.Object,
			},
		},
	},
};
</script>

<script setup lang="ts">
import embed from "vega-embed";
import { inject, onMounted, Ref, ref, watch } from "vue";
import injectionKeys from "../injectionKeys";

const chartTargetEl: Ref<HTMLElement> = ref(null);
const fields = inject(injectionKeys.evaluatedFields);

const renderChart = async () => {
	if (!fields.value.spec) return;
	await embed(chartTargetEl.value, fields.value.spec);
};

watch(
	() => fields.value?.spec,
	(spec) => {
		if (!spec) return;
		renderChart();
	}
);

onMounted(() => {
	renderChart();
});
</script>

<style scoped>
@import "../renderer/sharedStyles.css";

.CoreSection {
	padding: 16px;
	border: 1px solid var(--separatorColor);
	border-radius: 8px;
	background-color: var(--containerBackgroundColor);
}

h2 {
	margin-bottom: 16px;
}
</style>
