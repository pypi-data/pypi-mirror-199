<script lang="ts">
import { computed, h, inject } from "vue";
import { Component, FieldType } from "../streamsyncTypes";
import ComponentProxy from "../renderer/ComponentProxy.vue";
import injectionKeys from "../injectionKeys";

const defaultRepeaterObject = {
	a: { name: "Bobby", age: 2 },
	b: { name: "Robert", age: 39 },
	c: { name: "Bob", age: 57 },
};

export default {
	streamsync: {
		name: "Repeater",
		description: "Repeat child components.",
		category: "Other",
		allowedChildrenTypes: ["inherit"],
		fields: {
			repeaterObject: {
				name: "Repeater Object",
				default: JSON.stringify(defaultRepeaterObject, null, 2),
				type: FieldType.Object,
			},
			keyVariable: {
				name: "Key variable name",
				default: "itemId",
				init: "itemId",
				type: FieldType.Text,
			},
			valueVariable: {
				name: "Value variable name",
				default: "item",
				init: "item",
				type: FieldType.Text,
			},
		},
	},
	setup(props, { slots }) {
		const ss = inject(injectionKeys.core);
		const componentId = inject(injectionKeys.componentId);
		const fields = inject(injectionKeys.evaluatedFields);
		const renderProxiedComponent = inject(
			injectionKeys.renderProxiedComponent
		);

		const children = computed(() => ss.getComponents(componentId, true));
		const getRepeatedChildrenVNodes = () => {
			if (typeof fields.value.repeaterObject !== "object") {
				return [];
			}

			const repeatedChildrenVNodes = Object.values(
				fields.value.repeaterObject
			).map((item, itemIndex) =>
				children.value.map((childComponent) =>
					renderProxiedComponent(childComponent.id, itemIndex)
				)
			);
			return repeatedChildrenVNodes;
		};

		return () => {
			return h(
				"div",
				{
					class: "CoreRepeater",
					"data-streamsync-container": "",
				},
				children.value.length == 0 ||
					Object.keys(fields.value.repeaterObject).length == 0
					? slots.default({})
					: getRepeatedChildrenVNodes()
			);
		};
	},
};
</script>
<style scoped>
.CoreRepeater:not(.childless) {
	display: contents;
}

[data-streamsync-container].horizontal .CoreRepeater.childless {
	flex: 1 0 auto;
}
</style>
