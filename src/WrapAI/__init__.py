# WrapAI/__init__.py

import logging

# Create a logger for your library
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

# __all__ = ['Class']

def some_function():
    logger.debug("This is a debug message from my_library.")

# In use
from .utils.markdown import MarkdownToTextFromString
from .prompt_attributes import PromptAttributes, VeniceParameters
from .prompt_text import VeniceTextPrompt
from .prompt_chat import VeniceChatPrompt
from .prompt_library import PromptLibrary
from .prompt_template import PromptTemplate
from .prompt_response import PromptResponse
from .handlers import FILE_HANDLERS
from .wv_core import WEB_SEARCH_MODES, CUSTOM_SYSTEM_PROMPT
from .schema_document import DocumentManager
from .schema_json import SchemaBuilder, SchemaField, extract_schema_fields_from_json, reconcile_schema_fields
from .schema_parser import parse_response_with_schema


__all__ = [
    "MarkdownToTextFromString",
    "PromptAttributes",
    "VeniceParameters",
    "VeniceTextPrompt",
    "VeniceChatPrompt",
    "PromptLibrary",
    "PromptTemplate",
    "PromptResponse",
    "FILE_HANDLERS",
    "WEB_SEARCH_MODES",
    "CUSTOM_SYSTEM_PROMPT",
    "DocumentManager",
    "SchemaBuilder",
    "SchemaField",
    "extract_schema_fields_from_json",
    "reconcile_schema_fields",
    "parse_response_with_schema"
]
