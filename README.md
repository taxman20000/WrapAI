# WrapAI

**Version: 0.2.0**

Modular Python library for AI prompt engineering, chat memory, schema validation, and structured document workflows—designed for seamless use with Venice AI, OpenAI, and similar APIs.

[GitHub: https://github.com/WrapTools/WrapAI](https://github.com/WrapTools/WrapAI)

---

## Features

* Prompt templates with placeholders, file inputs, and variable substitution.
* Flexible prompt attributes for Venice, OpenAI, or custom APIs.
* Conversation memory (auto-trimming, summarization, token limits).
* Structured schema building and response validation.
* Extensible file handler system (TXT, PDF, easily add more).
* Markdown/text utilities for extraction and cleaning.

---

## Installation

Clone and install in editable mode:

```bash
git clone https://github.com/WrapTools/WrapAI.git
cd WrapAI
pip install -e .
```

**Note:** Require additional WrapLibraries (install with `pip install -e .` from each repo):

* \[Link to WrapDataclass]
* https://github.com/WrapTools/WrapCapPDF (for PDF functionality)

---

## API Keys for Examples

To run the examples, create a `.env` file inside the `examples` directory with the following contents:

VENICE_API_KEY=<your_api_key>
VENICE_API_KEY_ADMIN=<your_api_key>
OPENAI_API_KEY=<your_api_key>

Replace `<your_api_key>` with your actual API keys for Venice and OpenAI.  
This allows the example scripts to authenticate and run successfully.

---

## Quick Example

```python
from WrapAI.prompt_text import VeniceTextPrompt
from WrapAI.prompt_attributes import VeniceParameters

api_key = "YOUR_VENICE_API_KEY"
venice = VeniceTextPrompt(api_key, "venice-uncensored")
venice.set_attributes(temperature=0.2, venice_parameters=VeniceParameters(enable_web_search="auto"))
response = venice.prompt("What is the capital of Italy?")
print(response.response)  # Rome
```

---

## Extending File Handlers

Add new file type support by creating a `register()` function in a new `handlers/` module, and include it in `handlers/__init__.py`.

---

## Contributing & License

Contributions are welcome!
License: MIT (see `LICENSE`).

---


**Author:**
David — [dave@chatrecall.com](mailto:dave@chatrecall.com)


