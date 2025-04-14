# prompt_attributes.py

from dataclasses import dataclass, field
from typing import Optional, Any, Dict, List

import logging

# Logger Configuration
logger = logging.getLogger(__name__)

from WrapDataclass.core.base import BaseModel

from .wv_core import WEB_SEARCH_MODES

@dataclass
class VeniceParameters(BaseModel):
    enable_web_search: Optional[str] = None
    include_venice_system_prompt: Optional[bool] = None
    character_slug: Optional[str] = None
    response_format: Optional[Dict[str, Any]] = None

    def __post_init__(self):
        if self.enable_web_search is not None and self.enable_web_search not in WEB_SEARCH_MODES:
            raise ValueError(f"enable_web_search must be one of {WEB_SEARCH_MODES}, got '{self.enable_web_search}'")

@dataclass
class PromptAttributes(BaseModel):
    temperature: Optional[float] = None
    top_p: Optional[float] = None
    frequency_penalty: Optional[float] = None
    presence_penalty: Optional[float] = None
    max_completion_tokens: Optional[int] = None
    stop: Optional[List[str]] = None
    stream: Optional[bool] = None
    n: Optional[int] = None
    user: Optional[str] = None
    parallel_tool_calls: Optional[bool] = None
    tools: Optional[Any] = None
    tool_choice: Optional[Dict[str, Any]] = None
    stream_options: Optional[Dict[str, Any]] = None
    venice_parameters: VeniceParameters = field(default_factory=VeniceParameters)

    def __post_init__(self):
        if self.temperature is not None and not (0 <= self.temperature <= 2):
            raise ValueError("temperature must be between 0 and 2.")
        if self.top_p is not None and not (0 <= self.top_p <= 1):
            raise ValueError("top_p must be between 0 and 1.")
        if self.frequency_penalty is not None and not (-2 <= self.frequency_penalty <= 2):
            raise ValueError("frequency_penalty must be between -2 and 2.")
        if self.presence_penalty is not None and not (-2 <= self.presence_penalty <= 2):
            raise ValueError("presence_penalty must be between -2 and 2.")

        # Convert dict to VeniceParameters if passed as dict
        if isinstance(self.venice_parameters, dict):
            logger.warning(
                "PromptAttributes: 'venice_parameters' was provided as a dict. Converting to VeniceParameters dataclass."
            )
            self.venice_parameters = VeniceParameters.from_dict(self.venice_parameters)
