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

    print("Get details on a model")
    details = venice_models.get_model_detail("venice-uncensored")
    print(details)
    print(details["response_schema"])
    print(details["reasoning"])

    # Get dictionary of model names and their token counts
    model_tokens_dict = venice_models.get_model_tokens_dict()
    # print("Model Tokens Dictionary:", model_tokens_dict)
    # Create a PrettyPrinter instance
    pp = pprint.PrettyPrinter(indent=4)
    print("Model Tokens Dictionary:")
    pp.pprint(model_tokens_dict)

    # Get full model detail dictionary
    print("\nModel Detail Dictionary:")
    model_detail_dict = venice_models.get_model_detail_dict()
    pp.pprint(model_detail_dict)

    # Get token count for a specific model
    specific_model_name = "deepseek-r1-671b"
    tokens = venice_models.get_tokens_by_model_name(specific_model_name)
    print(f"Available Tokens for {specific_model_name}:", tokens)

    print('All model data')
    pp.pprint(venice_models.models_data)
