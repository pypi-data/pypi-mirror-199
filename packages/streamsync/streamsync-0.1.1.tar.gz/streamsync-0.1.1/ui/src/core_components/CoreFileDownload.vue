<template>
	<div class="CoreFileDownload">
		<button v-on:click="download">
			{{ fields.text }}
		</button>
	</div>
</template>

<script lang="ts">
import { FieldType } from "../streamsyncTypes";
import {
	buttonColor,
	buttonShadow,
	buttonTextColor,
	separatorColor,
} from "../renderer/sharedStyleFields";

export default {
	streamsync: {
		name: "File Download",
		description: "Enables the user to download a file.",
		category: "Other",
		fields: {
			text: {
				name: "Text",
				init: "Download",
				default: "Download",
				type: FieldType.Text,
			},
			data: {
				name: "Data",
				default: "data:text/plain;base64,aGVsbG8gd29ybGQ=",
				type: FieldType.Text,
				desc: "A valid data URL. Alternatively, you can provide a state reference to a FileWrapper or a BytesWrapper.",
			},
			fileName: {
				name: "File name",
				init: "myfile.csv",
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
import injectionKeys from "../injectionKeys";
const fields = inject(injectionKeys.evaluatedFields);

const download = () => {
	const el = document.createElement("a");
	el.href = fields.value.data;
	el.download = fields.value.fileName;
	el.click();
};
</script>

<style scoped>
@import "../renderer/sharedStyles.css";
</style>
