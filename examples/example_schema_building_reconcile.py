# example_schema_builder.py

import logging
import re
import json
from typing import List

from WrapAI import SchemaField, SchemaBuilder, extract_schema_fields_from_json


# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(name)s - %(levelname)s - %(message)s (line: %(lineno)d)',
    handlers=[logging.StreamHandler()]
)

# Reconcile logic
def reconcile_schema_fields(
    field_names: List[str],
    schema_json: dict = None,
    schema_name: str = "PromptDrivenSchema",
    default_type: str = "string",
    default_required: bool = True,
    return_builder: bool = True
):
    if schema_json is None:
        schema_json = {
            "type": "json_schema",
            "json_schema": {
                "name": schema_name,
                "schema": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            }
        }

    schema = schema_json["json_schema"]["schema"]
    properties = schema.get("properties", {})

    updated_properties = {}
    updated_required = []

    for name in field_names:
        if name in properties:
            updated_properties[name] = properties[name]
        else:
            updated_properties[name] = {
                "type": default_type,
                "description": f"Auto-added field for '{name}'"
            }
        if default_required:
            updated_required.append(name)

    schema["properties"] = updated_properties
    schema["required"] = updated_required
    schema_json["json_schema"]["schema"] = schema

    if return_builder:
        builder = SchemaBuilder(schema_json["json_schema"]["name"])
        builder.properties = updated_properties
        builder.required = updated_required
        return builder

    return schema_json


# Prompt parser
def extract_placeholders(prompt: str) -> List[str]:
    return sorted(set(re.findall(r"%%(.*?)%%", prompt)))


# Example usage
if __name__ == "__main__":
    # Simulated prompt input
    prompt_text = """
    Generate a response that includes the following details:
    - Title: %%title%%
    - Score: %%score%%
    - Rank: %%rank%%
    - Is Active: %%is_active%%
    - Tags: %%tags%%
    """

    placeholder_names = extract_placeholders(prompt_text)
    print("Extracted placeholders from prompt:", placeholder_names)

    # Reconcile against an existing schema (or None)
    reconciled_schema = reconcile_schema_fields(placeholder_names)
    reconciled_schema.print_json()

    # Optional: reverse into SchemaFields
    print("\nReversed SchemaField list from ReconciledSchema:")
    reversed_fields = extract_schema_fields_from_json(reconciled_schema.build())
    for field in reversed_fields:
        print(field)
