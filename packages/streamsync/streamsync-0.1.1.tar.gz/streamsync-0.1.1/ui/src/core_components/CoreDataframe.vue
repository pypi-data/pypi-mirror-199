<template>
	<div class="CoreDataframe">
		<table v-if="!isEmpty">
			<thead>
				<tr>
					<th v-for="columnIndex in columnIndexes" :key="columnIndex">
						{{ columnIndex }}
					</th>
				</tr>
			</thead>
			<tbody>
				<tr v-for="rowIndex in rowIndexes" :key="rowIndex">
					<td v-for="columnName in columnIndexes" :key="columnName">
						{{ dfData[columnName][rowIndex] }}
					</td>
				</tr>
			</tbody>
		</table>
		<div class="empty" v-else>Empty dataframe.</div>
	</div>
</template>

<script lang="ts">
import { computed, inject } from "vue";
import { FieldCategory, FieldType } from "../streamsyncTypes";
import {
	primaryTextColor,
	secondaryTextColor,
	separatorColor,
} from "../renderer/sharedStyleFields";

const defaultDataframe = `
{
  "data": {
    "col_a": [1, 2, 3],
    "col_b": [4, 5, 6]
  },
  "metadata": {}
}`.trim();

export default {
	streamsync: {
		name: "Dataframe",
		description: "Displays and allows interactions with dataframes.",
		category: "Content",
		fields: {
			dataframe: {
				name: "Data",
				desc: "Must be a JSON object or a state reference to a Pandas dataframe.",
				type: FieldType.Object,
				default: defaultDataframe,
			},
			primaryTextColor,
			secondaryTextColor,
			separatorColor,
			dataframeBackgroundColor: {
				name: "Background",
				type: FieldType.Color,
				category: FieldCategory.Style,
				applyStyleVariable: true,
			},
			dataframeHeaderRowBackgroundColor: {
				name: "Header row background",
				type: FieldType.Color,
				category: FieldCategory.Style,
				default: "#f0f0f0",
				applyStyleVariable: true,
			},
		},
	},
};
</script>
<script setup lang="ts">
import injectionKeys from "../injectionKeys";

const fields = inject(injectionKeys.evaluatedFields);

const dfData = computed(() => fields.value?.dataframe?.data);

const columnIndexes = computed(() => {
	return Object.keys(dfData.value ?? {});
});

const isEmpty = computed(() => {
	const e = !dfData.value || columnIndexes.value.length == 0;
	return e;
});

const rowIndexes = computed(() => {
	const firstColumn = dfData.value[columnIndexes.value[0]];
	const rowIndexes = Object.keys(firstColumn);
	return rowIndexes;
});
</script>

<style scoped>
@import "../renderer/sharedStyles.css";

.CoreDataframe {
	background: var(--dataframeBackgroundColor);
	font-size: 0.8rem;
	width: fit-content;
	max-width: 100%;
	max-height: 60vh;
	overflow: auto;
	border: 1px solid var(--separatorColor);
}

table {
	border-spacing: 0;
	border-collapse: separate;
}

th {
	position: sticky;
	top: 0;
	padding: 8px;
	color: var(--primaryTextColor);
	background-color: var(--dataframeHeaderRowBackgroundColor);
	border: 0.5px solid var(--separatorColor);
}

td {
	border: 0.5px solid var(--separatorColor);
	padding: 8px;
	color: var(--primaryTextColor);
}

td.rowIndex {
	color: var(--secondaryTextColor);
}
</style>
