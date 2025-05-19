# example_sent_prompt.py

from WrapAI.prompt_text import VeniceTextPrompt, OpenAITextPrompt
from WrapAI.prompt_library import PromptLibrary

# Configure Logging
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format = '%(name)s - %(levelname)s - %(message)s (line: %(lineno)d)',
    handlers=[
        logging.StreamHandler(),  # Log to console
        # logging.FileHandler('app.log')  # Log to file
    ]
)

from secret_loader import load_secret


# Choose which API to use
USE_VENICE = False  # Set to False to use OpenAI

if USE_VENICE:
    print("Using Venice")
    API_KEY_TYPE = "VENICE_API_KEY_ADMIN"
    MODEL = "venice-uncensored" # Not reasoning
    # MODEL = "qwen-2.5-qwq-32b" # Reasoning
    # PROMPT = "test_json"
    # PROMPT = "executive_order_evaluator_prompt_json"
    # PROMPT = "test_venice"
    PROMPT = "test_json"

    api_key = load_secret(API_KEY_TYPE)
    runner = VeniceTextPrompt(api_key=api_key, model=MODEL)
else:
    print("Using OpenAI")
    API_KEY_TYPE = "OPENAI_API_KEY"
    MODEL = "gpt-4.1-nano"
    OPENAI_BASE_URL = "https://api.openai.com/v1"
    # PROMPT = "test_openai"
    PROMPT = "test_json"

    api_key = load_secret(API_KEY_TYPE)
    runner = OpenAITextPrompt(api_key=api_key, model=MODEL, base_url=OPENAI_BASE_URL)



if __name__ == "__main__":
    library = PromptLibrary.from_json_file("prompts.json")
    prompt, system_prompt = library.get_prompt_with_system_prompt(PROMPT)
    # print("Prompt")
    # print(prompt)

    # Set attributes based on the prompt defaults
    runner.set_attributes(**prompt.default_attributes.to_dict())

    # Run Prompt
    response = runner.prompt(prompt.prompt_text, system_prompt=prompt.prompt_system_text)

    # Output
    print("\n🧠 Think:\n", response.think or "N/A")
    print("\n💬 Response:\n", response.response or "N/A")

    attrs = response.as_prompt_attributes
    print("\n🎛️ Parameters:")
    print(f"- Temperature: {attrs.temperature}")

    # Only show Venice parameters if using Venice
    if USE_VENICE:
        print(f"- Web Search: {attrs.venice_parameters.enable_web_search}")

    print("\n📊 Token Usage:")
    print(f"- Total: {response.usage.get('total_tokens', 'N/A')}")
    print(f"- Prompt: {response.usage.get('prompt_tokens', 'N/A')}")
    print(f"- Completion: {response.usage.get('completion_tokens', 'N/A')}")
