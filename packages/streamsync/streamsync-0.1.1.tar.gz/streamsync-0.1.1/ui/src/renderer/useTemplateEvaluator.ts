import { Core, FieldType, InstancePath } from "../streamsyncTypes";

export function useTemplateEvaluator(ss: Core) {
	const templateRegex = /[\\]?@{([\w\s.]*)}/g;

	function getContextData(instancePath: InstancePath) {
		const context = {};

		for (let i = 0; i < instancePath.length - 1; i++) {
			const pathItem = instancePath[i];
			const { componentId } = pathItem;
			const { type } = ss.getComponentById(componentId);
			if (type !== "repeater") continue;
			if (i + 1 >= instancePath.length) continue;
			const repeaterInstancePath = instancePath.slice(0, i + 1);
			const nextInstancePath = instancePath.slice(0, i + 2);
			const { instanceNumber } = nextInstancePath.at(-1);

			const repeaterObject = evaluateField(
				repeaterInstancePath,
				"repeaterObject"
			);
			const repeaterEntries = Object.entries(repeaterObject);
			const keyVariable = evaluateField(
				repeaterInstancePath,
				"keyVariable"
			);
			const valueVariable = evaluateField(
				repeaterInstancePath,
				"valueVariable"
			);

			context[keyVariable] = repeaterEntries[instanceNumber][0];
			context[valueVariable] = repeaterEntries[instanceNumber][1];
		}

		return context;
	}

	function evaluateTemplate(
		template: string,
		instancePath: InstancePath
	): any {
		if (template === undefined || template === null) return null;
		let monoMatch: any;

		const contextData = getContextData(instancePath);

		const evaluatedTemplate = template.replace(
			templateRegex,
			(match, captured) => {
				if (match.charAt(0) == "\\") return match.substring(1); // Escaped @, don't evaluate, return without \
				const expr = captured.trim();
				if (!expr) return;

				const exprValue = ss.evaluateExpression(expr, contextData);
				if (typeof exprValue === "undefined") return;

				if (expr === match) {
					monoMatch = exprValue;
					return;
				}

				if (typeof exprValue == "object") {
					return JSON.stringify(exprValue);
				}

				return exprValue;
			}
		);

		const value =
			typeof monoMatch == "undefined" ? evaluatedTemplate : monoMatch;
		return value;
	}

	function getEvaluatedFields(
		instancePath: InstancePath
	): Record<string, any> {
		const { componentId } = instancePath.at(-1);
		const component = ss.getComponentById(componentId);
		if (!component) return;
		const evaluatedFields: Record<string, any> = {};
		const { fields } = ss.getComponentDefinition(component.type);
		if (!fields) return;
		Object.keys(fields).forEach((fieldKey) => {
			evaluatedFields[fieldKey] = evaluateField(instancePath, fieldKey);
		});

		return evaluatedFields;
	}

	function evaluateField(instancePath: InstancePath, fieldKey: string) {
		const { componentId } = instancePath.at(-1);
		const component = ss.getComponentById(componentId);
		const { fields } = ss.getComponentDefinition(component.type);
		const contentValue = component.content?.[fieldKey];
		const defaultValue = fields[fieldKey].default;
		const evaluated = evaluateTemplate(contentValue, instancePath);
		const fieldType = fields[fieldKey].type;
		if (fieldType == FieldType.Object || fieldType == FieldType.KeyValue) {
			if (!evaluated) {
				if (defaultValue) return JSON.parse(defaultValue);
				return null;
			}
			if (typeof evaluated !== "string") return evaluated;
			let parsedValue: any;
			try {
				parsedValue = JSON.parse(evaluated);
			} catch {
				if (defaultValue) return JSON.parse(defaultValue);
				return null;
			}
			return parsedValue;
		} else if (fieldType == FieldType.Number) {
			const n = parseFloat(evaluated);
			if (typeof n === undefined || Number.isNaN(n))
				return parseFloat(defaultValue);
			return n;
		} else if (fieldType == FieldType.Text || FieldType.Color) {
			const isValueEmpty =
				typeof contentValue == "undefined" ||
				contentValue === null ||
				contentValue === "";
			if (isValueEmpty) return defaultValue;
			return evaluated;
		}
	}

	return {
		getEvaluatedFields,
	};
}
