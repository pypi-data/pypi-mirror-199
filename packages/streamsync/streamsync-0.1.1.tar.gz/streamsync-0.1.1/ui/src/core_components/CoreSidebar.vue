<template>
	<div
		class="CoreSidebar"
		:style="rootStyle"
		:class="{
			collapsed: isCollapsed,
		}"
	>
		<div class="collapserContainer">
			<div class="collapser" v-on:click="toggleCollapsed">
				<IconGen
					class="collapserArrow"
					icon-key="collapseArrow"
				></IconGen>
			</div>
		</div>
		<div class="container" data-streamsync-container>
			<slot></slot>
		</div>
	</div>
</template>

<script lang="ts">
import { FieldCategory, FieldType } from "../streamsyncTypes";
import * as sharedStyleFields from "../renderer/sharedStyleFields";

export default {
	streamsync: {
		name: "Sidebar",
		description:
			"Organises components in a sidebar. Its parent must be a Page.",
		positionless: true,
		allowedParentTypes: ["page"],
		allowedChildrenTypes: ["*"],
		category: "Layout",
		fields: {
			startCollapsed: {
				name: "Start collapsed",
				type: FieldType.Text,
				category: FieldCategory.Style,
				default: "no",
				options: {
					yes: "yes",
					no: "no",
				},
			},
			sidebarBackgroundColor: {
				name: "Background",
				type: FieldType.Color,
				category: FieldCategory.Style,
				applyStyleVariable: true,
				default: "rgba(255, 255, 255, 0.2)",
			},
			...sharedStyleFields,
		},
	},
};
</script>
<script setup lang="ts">
import { computed, inject, onMounted, Ref, ref } from "vue";
import injectionKeys from "../injectionKeys";
import IconGen from "../renderer/IconGen.vue";
const fields = inject(injectionKeys.evaluatedFields);

const isCollapsed: Ref<boolean> = ref(fields.value?.startCollapsed == "yes");

const toggleCollapsed = () => {
	isCollapsed.value = !isCollapsed.value;
};

const rendererTop = ref(0);

const getComponentRendererTop = () => {
	const rendererEl = document.querySelector(".ComponentRenderer");
	const { top: rendererTop } = rendererEl.getBoundingClientRect();
	return rendererTop;
};

const rootStyle = computed(() => {
	return {
		"max-height": `calc(100vh - ${rendererTop.value}px)`,
	};
});

onMounted(() => {
	rendererTop.value = getComponentRendererTop();
});
</script>

<style scoped>
@import "../renderer/sharedStyles.css";

.CoreSidebar {
	overflow: auto;
	padding: 16px;
	border-right: 1px solid var(--separatorColor);
	position: sticky;
	top: 0;
	background-color: transparent;
}

.CoreSidebar:not(.collapsed) {
	width: 20vw;
	max-width: 300px;
	background-color: var(--sidebarBackgroundColor);
}

.CoreSidebar.collapsed > .container {
	display: none;
}

.collapserContainer {
	display: flex;
	justify-content: right;
	margin-bottom: 16px;
}

.collapserContainer > .collapser {
	flex: 0 0 32px;
	min-width: 32px;
	border-radius: 16px;
	padding: 4px;
	display: flex;
	align-items: center;
	justify-content: center;
	stroke: var(--primaryTextColor);
	border: 1px solid var(--separatorColor);
}

.collapserContainer .collapserArrow {
	transition: all 0.5s ease-in-out;
	transform: rotate(0deg);
}

.CoreSidebar.collapsed .collapserArrow {
	transform: rotate(180deg);
}

.collapserContainer > .collapser:hover {
	background: var(--separatorColor);
}
</style>
