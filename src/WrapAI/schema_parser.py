# schema_parser.py

from typing import Any, Dict
import logging

# Logger Configuration
logger = logging.getLogger(__name__)

from .schema_json import extract_schema_fields_from_json, SchemaField


def parse_response_with_schema(
    response_json: dict,
    schema_json: dict,
    include_missing_optionals: bool = False
) -> dict:
    """
    Parse a response JSON object using a schema definition and return a typed dict.
    Optionally include missing optional fields as `None`.

    :param response_json: The raw JSON dictionary returned by the AI or API.
    :param schema_json: The schema used to validate and extract expected fields.
    :param include_missing_optionals: If True, include missing optional fields with value None.
    :return: A new dict matching the schema.
    """
    parsed = {}
    fields = extract_schema_fields_from_json(schema_json)

    for field in fields:
        value = response_json.get(field.name)

        # if field.required and value is None:
        #     raise ValueError(f"Missing required field: {field.name}")

        if value is None:
            if field.required:
                raise ValueError(f"Missing required field: {field.name}")
            elif include_missing_optionals:
                parsed[field.name] = None
            continue

        expected_type = field.type
        if expected_type == "array":
            if not isinstance(value, list):
                raise ValueError(f"Field '{field.name}' should be a list.")
        elif expected_type == "string":
            if not isinstance(value, str):
                raise ValueError(f"Field '{field.name}' should be a string.")
        elif expected_type == "integer":
            if not isinstance(value, int):
                raise ValueError(f"Field '{field.name}' should be an integer.")
        elif expected_type == "number":
            if not isinstance(value, (int, float)):
                raise ValueError(f"Field '{field.name}' should be a number.")
        elif expected_type == "boolean":
            if not isinstance(value, bool):
                raise ValueError(f"Field '{field.name}' should be a boolean.")
        elif expected_type == "enum":
            if value not in field.enum_values:
                raise ValueError(f"Invalid value '{value}' for enum field '{field.name}'.")
        elif expected_type == "const":
            if value != field.value:
                raise ValueError(f"Field '{field.name}' must be '{field.value}'.")

        parsed[field.name] = value

    return parsed
