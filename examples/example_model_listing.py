from WrapAI.info.models import VeniceModels
from secret_loader import load_secret

import pprint

from WrapAI.info.models import VeniceModels
from secret_loader import load_secret
import pprint

# Example usage:
if __name__ == "__main__":
    api_key = load_secret("VENICE_API_KEY")

    venice_models = VeniceModels(api_key)
    venice_models.fetch_models()  # Fetch and store models data

    # Get all model names
    model_names = venice_models.get_model_names()
    print("Model Names:", model_names)

    print("\nGet full detail for one model (venice-uncensored):")
    all_models = venice_models.get_full_model_detail_dict()
    model_detail = all_models.get("venice-uncensored", {})
    pprint.pprint(model_detail)

    # Example: Access nested capabilities directly from raw detail
    caps = model_detail.get("model_spec", {}).get("capabilities", {})
    print("Response Schema Supported:", caps.get("supportsResponseSchema"))
    print("Reasoning Supported:", caps.get("supportsReasoning"))

    print("\nAll models - full detail dict (recommended usage):")
    pprint.pprint(all_models)

    print("\n--- DEPRECATED methods ---")
    print("The following methods are deprecated and will be removed in a future release:")
    print("- get_model_detail()")
    print("- get_model_tokens_dict()")
    print("- get_model_detail_dict()")
    print("- get_model_detail_dict_full()")
    print("- get_tokens_by_model_name()")
    print("Please use get_full_model_detail_dict() and extract the info you need directly.")

    # Optional: If you want to keep showing how to migrate
    # For example, to get available tokens for a model:
    model_id = "deepseek-r1-671b"
    tokens = all_models.get(model_id, {}).get("model_spec", {}).get("availableContextTokens", "N/A")
    print(f"\nAvailable Tokens for {model_id}:", tokens)

    # Pretty-print all raw model data if needed
    print('\nAll model data (raw, from venice_models.models_data):')
    pprint.pprint(venice_models.models_data)

