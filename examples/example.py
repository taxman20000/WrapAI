# example.py

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

from pathlib import Path
import json
from WrapAI.prompt_template import PromptTemplate
from WrapAI.prompt_library import PromptLibrary

def debug_prompt_structure(prompt):
    print("\n🔍 Prompt Structure Debug")

    print(f"Prompt type: {type(prompt)}")
    print(f"Prompt text: {prompt.prompt_text[:60]}...")  # Trim for readability

    attrs = prompt.default_attributes
    print(f"Attributes type: {type(attrs)}")
    print(f"Temperature: {attrs.temperature}")
    print(f"Top_p: {attrs.top_p}")
    print(f"Presence Penalty: {attrs.presence_penalty}")

    v_params = attrs.venice_parameters
    print(f"Venice Parameters type: {type(v_params)}")
    print(f" - enable_web_search: {v_params.enable_web_search}")
    print(f" - include_venice_system_prompt: {v_params.include_venice_system_prompt}")
    print(f" - character_slug: {v_params.character_slug}")
    print(f" - response_format: {json.dumps(v_params.response_format, indent=2)}")



# Load the JSON file
json_path = Path("prompts.json")
with json_path.open("r", encoding="utf-8") as f:
    data = json.load(f)

# Convert each entry to PromptTemplate
prompts = {}
for key, val in data["data"].items():
    try:
        prompts[key] = PromptTemplate(**val)
    except Exception as e:
        print(f"❌ Failed to load prompt '{key}': {e}")

# Create a PromptLibrary instance
library = PromptLibrary(prompts=prompts)

# List prompts
print("Available Prompts:")
for name in library.list_prompts():
    print(" -", name)

# View a specific prompt
prompt = library.get_prompt("executive_order_summary_prompt")
if prompt:
    print("\nSummary Prompt Text (trimmed):")
    print(prompt.prompt_text[:300])  # Show part of the text

raw_prompt = data["data"]["test_json"]
prompt = PromptTemplate(**raw_prompt)
debug_prompt_structure(prompt)