<script lang="ts">
import { h, inject } from "vue";
import { FieldType } from "../streamsyncTypes";
import injectionKeys from "../injectionKeys";

const defaultStyle = {
	padding: "16px",
	"min-height": "64px",
	"min-width": "64px",
	"border-radius": "8px",
	background:
		"linear-gradient(90deg, rgba(41,207,0,1) 0%, rgba(145,231,78,1) 100%)",
};

export default {
	streamsync: {
		name: "HTML Element",
		description:
			"Creates discretionary HTML elements, which can serve as containers.",
		category: "Other",
		allowedChildrenTypes: ["*"],
		fields: {
			element: {
				name: "Element",
				default: "div",
				type: FieldType.Text,
			},
			styles: {
				name: "Styles",
				default: null,
				init: JSON.stringify(defaultStyle, null, 2),
				type: FieldType.Object,
			},
			attrs: {
				name: "Attributes",
				default: null,
				type: FieldType.Object,
			},
		},
	},
	setup(props, { slots }) {
		const fields = inject(injectionKeys.evaluatedFields);
		return () => {
			return h(
				fields.value.element,
				{
					...fields.value.attrs,
					"data-streamsync-container": "",
					style: fields.value.styles,
				},
				slots.default(0)
			);
		};
	},
};
</script>
