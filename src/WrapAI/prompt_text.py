# prompt_text.py

import logging

logger = logging.getLogger(__name__)

CHAT_COMPLETION = "/chat/completions"

import json
import logging
import hashlib
import requests
from pathlib import Path
from typing import Optional, Dict, List, Any

from .prompt_attributes import OpenAIPromptAttributes, VenicePromptAttributes, VeniceParameters
from .prompt_response import PromptResponse
from .utils.markdown import MarkdownToText
from .wv_core import BASE_URL


class OpenAITextPrompt:
    def __init__(self, api_key: str, model: str, base_url: str = "https://api.openai.com/v1"):
        self.api_key = api_key
        self.model = model
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        self.attributes = OpenAIPromptAttributes()
        self.parsed_response: Optional[PromptResponse] = None
        self.last_user_prompt: str = ""
        self.last_system_prompt: str = ""

    def set_attributes(self, **kwargs):
        """Dynamically assign attributes."""
        for key, value in kwargs.items():
            if hasattr(self.attributes, key):
                setattr(self.attributes, key, value)
            else:
                logger.warning(f"Unknown attribute '{key}' ignored.")

    def prompt(self, user_prompt: str, system_prompt: str = "You are a helpful assistant.", messages=None) -> Optional[PromptResponse]:
        self.last_user_prompt = user_prompt
        self.last_system_prompt = system_prompt

        if messages is None:
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]

        payload = {
            "model": self.model,
            "messages": messages,
            **self.attributes.to_dict(skip_none=True)
        }

        try:
            response = requests.post(
                f"{self.base_url}{CHAT_COMPLETION}",
                headers=self.headers,
                json=payload,
                timeout=300
            )
            logger.debug(f"API response status: {response.status_code}")
            data = response.json()

            if "error" in data:
                logger.error(f"API Error: {data['error']}")
                return None

            self.parsed_response = self.parse_response(data)
            return self.parsed_response

        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {e}")
            return None

    def parse_response(self, response_json: dict) -> PromptResponse:
        content = response_json.get('choices', [{}])[0].get('message', {}).get('content', '')
        think, response = "", ""

        if '</think>' in content:
            parts = content.split('</think>', 1)
            think = parts[0].replace('<think>', '').strip()
            response = parts[1].strip()
        else:
            response = content.strip()

        return PromptResponse(
            model=response_json.get('model'),
            created=response_json.get('created'),
            usage=response_json.get('usage', {}),
            think=think,
            response=response.replace('<think>', '').replace('</think>', ''),
            citations=[],  # OpenAI doesn't have citations
            parameters=self.attributes.to_dict(skip_none=True),
            system_prompt=self.last_system_prompt,
            user_prompt=self.last_user_prompt
        )

    # Accessors
    def get_response(self) -> str:
        return self.parsed_response.response if self.parsed_response else ""

    def get_think(self) -> str:
        return self.parsed_response.think if self.parsed_response else ""

    def get_model(self) -> str:
        return self.parsed_response.model if self.parsed_response else "N/A"

    def get_usage(self) -> Dict:
        return self.parsed_response.usage if self.parsed_response else {}

    # Saving
    def save_all(self, file_path: str | Path):
        if not self.parsed_response:
            logger.warning("No response to save.")
            return
        file_path = Path(file_path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        self.parsed_response.to_json(file_path, app_name="OpenAIPrompt", data_version="1.0")

    def save_response(self, file_path: str | Path):
        response = self.get_response()
        if response:
            file_path = Path(file_path)
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(response, encoding="utf-8")

    def save_text_response(self, md_file_path: str | Path, output_path: str | Path):
        try:
            md_handler = MarkdownToText(md_file_path)
            md_handler.save_clean_text(output_path)
            logger.info(f"Saved clean text to {output_path}")
        except Exception as e:
            logger.error(f"Error saving clean text: {e}")

    # Hashing
    def get_structured_payload_for_hash(self, document_id: str, user_prompt: str, system_prompt: str, user_prompt_type="request") -> dict:
        return {
            "document_id": document_id,
            "system_prompt": system_prompt,
            user_prompt_type: {
                "model": self.model,
                "user_prompt": user_prompt,
                "parameters": self.attributes.to_dict(skip_none=True)
            }
        }

    def get_hash(self, structured_payload: dict) -> str:
        return hashlib.sha256(json.dumps(structured_payload, sort_keys=True).encode()).hexdigest()


class VeniceTextPrompt(OpenAITextPrompt):
    def __init__(self, api_key: str, model: str, base_url: str = BASE_URL):
        super().__init__(api_key, model, base_url)
        # Replace the OpenAI attributes with Venice attributes
        self.attributes = VenicePromptAttributes()

    def set_attributes(self, **kwargs):
        """Dynamically assign attributes or nested VeniceParameters."""
        for key, value in kwargs.items():
            if hasattr(self.attributes, key):
                if key == "venice_parameters":
                    if isinstance(value, dict):
                        self.attributes.venice_parameters = VeniceParameters(**value)
                    elif isinstance(value, VeniceParameters):
                        self.attributes.venice_parameters = value
                else:
                    setattr(self.attributes, key, value)
            else:
                logger.warning(f"Unknown attribute '{key}' ignored.")

    def prompt(self, user_prompt: str, system_prompt: str = "You are a helpful assistant.", messages=None,
               response_format: Optional[Dict[str, Any]] = None) -> Optional[PromptResponse]:

        self.last_user_prompt = user_prompt
        self.last_system_prompt = system_prompt

        if messages is None:
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]

        # Create the base payload without venice_parameters
        payload = {
            "model": self.model,
            "messages": messages,
            **{
                k: v for k, v in self.attributes.to_dict(skip_none=True).items()
                if k != "venice_parameters"
            }
        }

        # Add venice_parameters if they exist
        venice_data = self.attributes.venice_parameters.to_dict(skip_none=True)
        if venice_data:
            payload["venice_parameters"] = venice_data

        # Add response_format at the top level if provided
        if response_format:
            payload["response_format"] = response_format

        print("Payload")
        print(payload)

        try:
            response = requests.post(
                f"{self.base_url}{CHAT_COMPLETION}",
                headers=self.headers,
                json=payload,
                timeout=300
            )
            logger.debug(f"API response status: {response.status_code}")
            data = response.json()

            if "error" in data:
                logger.error(f"API Error: {data['error']}")
                return None

            self.parsed_response = self.parse_response(data)
            return self.parsed_response

        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {e}")
            return None

    def parse_response(self, response_json: dict) -> PromptResponse:
        # Override to include Venice-specific fields like citations
        content = response_json.get('choices', [{}])[0].get('message', {}).get('content', '')
        think, response = "", ""

        if '</think>' in content:
            parts = content.split('</think>', 1)
            think = parts[0].replace('<think>', '').strip()
            response = parts[1].strip()
        else:
            response = content.strip()

        return PromptResponse(
            model=response_json.get('model'),
            created=response_json.get('created'),
            usage=response_json.get('usage', {}),
            think=think,
            response=response.replace('<think>', '').replace('</think>', ''),
            citations=response_json.get("venice_parameters", {}).get("web_search_citations", []),
            parameters=self.attributes.to_dict(skip_none=True),
            system_prompt=self.last_system_prompt,
            user_prompt=self.last_user_prompt
        )

    def save_all(self, file_path: str | Path):
        if not self.parsed_response:
            logger.warning("No response to save.")
            return
        file_path = Path(file_path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        self.parsed_response.to_json(file_path, app_name="VenicePrompt", data_version="1.0")

