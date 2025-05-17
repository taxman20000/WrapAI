# models.py

import requests
import logging

from ..wv_core import BASE_URL

# Logger Configuration
logger = logging.getLogger(__name__)


class VeniceModels:
    def __init__(self, api_key, base_url=BASE_URL):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {"Authorization": f"Bearer {self.api_key}"}
        self.models_data = []  # To store models data after fetching

    # Fetch method
    def fetch_models(self):
        """Fetches the models from the API and stores them in the instance."""
        url = f"{self.base_url}/models"
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()  # Raise an exception for HTTP errors
            response_json = response.json()
            self.models_data = response_json.get("data", [])
        except requests.exceptions.RequestException as e:
            logger.error(f"An error occurred: {e}")
            self.models_data = []

    # Get methods
    def get_model_names(self):
        """Returns a list of model names (IDs)."""
        return [model.get("id", "N/A") for model in self.models_data]

    def get_model_tokens_dict(self):
        """Returns a dictionary mapping model names to their available context tokens."""
        return {
            model.get("id", "N/A"): model.get("model_spec", {}).get("availableContextTokens", "N/A")
            for model in self.models_data
        }

    def get_model_detail_dict(self):
        """
        Returns a dictionary mapping model names to a single formatted string with:
        tokens, reasoning, response_schema, web_search
        Example:
        {
            "llama-3.3-70b": "tokens: 65536, reasoning: False, response_schema: False, web_search: True"
        }
        """
        detail_dict = {}
        for model in self.models_data:
            model_id = model.get("id", "N/A")
            spec = model.get("model_spec", {})
            caps = spec.get("capabilities", {})

            tokens = spec.get("availableContextTokens", "N/A")
            reasoning = caps.get("supportsReasoning", False)
            schema = caps.get("supportsResponseSchema", False)
            web = caps.get("supportsWebSearch", False)

            detail_str = (
                f"tokens: {tokens}, reasoning: {reasoning}, response_schema: {schema}, web_search: {web}"
            )

            detail_dict[model_id] = detail_str
        return detail_dict

    def get_tokens_by_model_name(self, model_name):
        """Returns the available context tokens for a specific model name."""
        for model in self.models_data:
            if model.get("id") == model_name:
                return model.get("model_spec", {}).get("availableContextTokens", "N/A")
        return "Model not found"

    def get_model_detail(self, model_name):
        """
               Returns a dictionary of detailed attributes for the given model name.
               Example:
               {
                   "id": "llama-3.3-70b",
                   "tokens": 65536,
                   "reasoning": True,
                   "response_schema": False,
                   "web_search": True
               }
               """
        for model in self.models_data:
            if model.get("id") == model_name:
                spec = model.get("model_spec", {})
                caps = spec.get("capabilities", {})

                return {
                    "id": model.get("id", "N/A"),
                    "tokens": spec.get("availableContextTokens", "N/A"),
                    "reasoning": caps.get("supportsReasoning", False),
                    "response_schema": caps.get("supportsResponseSchema", False),
                    "web_search": caps.get("supportsWebSearch", False),
                }

        return {"error": "Model not found"}