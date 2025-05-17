# example_schema_builder.py
# Configure Logging
import logging

logging.basicConfig(
    level=logging.INFO,
    format = '%(name)s - %(levelname)s - %(message)s (line: %(lineno)d)',
    handlers=[
        logging.StreamHandler(),  # Log to console
        # logging.FileHandler('app.log')  # Log to file
    ]
)

from WrapAI import (SchemaField, SchemaBuilder, extract_schema_fields_from_json, PromptTemplate, schema_json, reconcile_schema_fields,
                    parse_response_with_schema)


# Example usage:
if __name__ == "__main__":
    # Recreate the LeapYearExplanation schema
    leap_year_schema = SchemaBuilder("LeapYearExplanation")
    leap_year_schema.add_string_property("explanation")
    leap_year_schema.add_integer_property("days_in_nonleap_year")
    leap_year_schema.add_integer_property("days_in_leap_year")

    print("LeapYearExplanation Schema:")
    leap_year_schema.print_json()

    # Create a document evaluation schema
    doc_eval_schema = SchemaBuilder("DocumentEvaluationSchema")
    doc_eval_schema.add_number_property("relevance_score", description="Score from 1.0-10.0 indicating relevance")
    doc_eval_schema.add_number_property("correspondence_score", description="Score from 1.0-10.0 indicating correspondence")
    doc_eval_schema.add_number_property("divergence_score", description="Score from 1.0-10.0 indicating divergence")
    doc_eval_schema.add_integer_property("match_confidence", description="Integer from 0-100 indicating confidence")
    doc_eval_schema.add_array_property("scoring_anchors", description="Key phrases from the document")
    doc_eval_schema.add_array_property("reasons", description="Document quotes that match criteria")
    doc_eval_schema.add_string_property("explanation", description="Reasoning for the scores")

    print("\nDocumentEvaluationSchema:")
    doc_eval_schema.print_json()

    # Test full usage: enums, booleans, constants, optional fields, nested schema
    safe_schema = SchemaBuilder("SafeSchema")
    safe_schema.add_enum_property("category", ["news", "blog", "report"], description="Type of document")
    safe_schema.add_boolean_property("is_verified", description="Indicates if the document was verified")
    safe_schema.add_string_property("title", description="Document title")
    safe_schema.add_const_property("version", "1.0", description="Schema version")

    # Optional property (not required)
    safe_schema.add_optional_property("notes", {
        "type": "string",
        "description": "Optional developer notes"
    })

    # Nested object via SchemaBuilder
    metadata_schema = SchemaBuilder("Metadata")
    metadata_schema.add_string_property("author", description="Name of the author")
    metadata_schema.add_string_property("date_published", description="Publication date")

    safe_schema.add_nested_schema_property("metadata", metadata_schema, description="Metadata information")

    print("\nSafeSchema:")
    safe_schema.print_json()

    doc_eval_fields = [
        SchemaField(name="relevance_score", type="number", description="Score from 1.0-10.0 indicating relevance"),
        SchemaField(name="correspondence_score", type="number", description="Score from 1.0-10.0 indicating correspondence"),
        SchemaField(name="divergence_score", type="number", description="Score from 1.0-10.0 indicating divergence"),
        SchemaField(name="match_confidence", type="integer", description="Integer from 0-100 indicating confidence"),
        SchemaField(name="scoring_anchors", type="array", item_type="string", description="Key phrases from the document"),
        SchemaField(name="reasons", type="array", item_type="string", description="Document quotes that match criteria"),
        SchemaField(name="explanation", type="string", description="Reasoning for the scores"),
    ]

    doc_eval_schema = SchemaBuilder("DocumentEvaluationSchema").load_properties(doc_eval_fields)
    doc_eval_schema.print_json()

    print("\nReversed SchemaField list from DocumentEvaluationSchema JSON:")
    doc_eval_json = doc_eval_schema.build()
    reversed_fields = extract_schema_fields_from_json(doc_eval_json)
    for field in reversed_fields:
        print(field)

    print("\n\n\n\nTest JSON")
    test_fields = [
        SchemaField(name="title", type="string", description="Title of the item"),
        SchemaField(name="score", type="number", description="Floating-point score between 0 and 10"),
        SchemaField(name="rank", type="integer", description="Integer rank position"),
        SchemaField(name="is_active", type="boolean", description="Is the item active?"),
        SchemaField(name="tags", type="array", item_type="string", description="List of tags associated with the item"),
    ]
    schema = SchemaBuilder("BasicTestSchema").clear_properties().load_properties(test_fields)
    schema_json = schema.build()
    schema.print_json()

    print("\n\n\nOutput Placeholder Integration with PromptTemplate")


    # Example prompt that includes @@ output fields
    output_fields = ["title", "score", "rank", "tags", "new_field"]
    print("Extracted output fields from prompt:", output_fields)

    # Reconcile output fields with the existing schema (remove is_active, add headline & confidence)
    reconciled_schema = reconcile_schema_fields(
        field_names=output_fields,
        schema_json=schema_json,
        return_builder=True
    )

    print("\nReconciled Schema after updating from prompt:")
    reconciled_schema.print_json()


test_response = {
    "summary": "This is a detailed markdown summary of the executive order...",
    "tags": ["Policy", "CivilRights", "ExecutiveOrder"]
}

fields = [
    SchemaField(name="summary", type="string", description="Markdown-formatted summary"),
    SchemaField(name="tags", type="array", item_type="string", description="One-word tags")
]

schema = SchemaBuilder("SummarySchema").clear_properties().load_properties(fields)
schema_json = schema.build()

parsed_data = parse_response_with_schema(test_response, schema_json)
print(parsed_data)
print("tags")
print(parsed_data["tags"])
