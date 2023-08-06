<template>
	<div
		class="CoreHorizontalStack horizontal"
		data-streamsync-container
		:class="[`justify-${fields.alignment}`]"
	>
		<slot></slot>
	</div>
</template>

<script lang="ts">
import { FieldType } from "../streamsyncTypes";

export default {
	streamsync: {
		name: "Horizontal Stack",
		description:
			"Stacks components horizontally, wrapping them if necessary.",
		allowedChildrenTypes: ["*"],
		category: "Layout",
		fields: {
			alignment: {
				name: "Alignment",
				default: null,
				init: "left",
				type: FieldType.Text,
				options: {
					left: "Left",
					center: "Center",
					right: "Right",
				},
			},
		},
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
.CoreHorizontalStack {
	flex-wrap: wrap;
	flex-direction: row;
	align-items: center;
}

.CoreHorizontalStack > .CoreHorizontalStack {
	flex-grow: 1;
}

.justify-left {
	justify-content: left;
}
.justify-center {
	justify-content: center;
}
.justify-right {
	justify-content: right;
}
</style>
