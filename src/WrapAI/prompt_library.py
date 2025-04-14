# prompt_library.py

from WrapDataclass.core.base import BaseModel
from dataclasses import dataclass, field
from typing import Dict, Optional
from .prompt_template import PromptTemplate


@dataclass
class PromptLibrary(BaseModel):
    prompts: Dict[str, PromptTemplate] = field(default_factory=dict)

    def list_prompts(self):
        return list(self.prompts.keys())

    def get_prompt(self, name: str) -> Optional[PromptTemplate]:
        return self.prompts.get(name)

    def remove_prompt(self, name: str):
        if name in self.prompts:
            del self.prompts[name]

    def add_prompt(self, name: str, prompt: PromptTemplate):
        self.prompts[name] = prompt

