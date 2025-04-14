# prompt_template.py

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Optional
import re
import hashlib
import logging

from WrapDataclass.core.base import BaseModel
from .prompt_attributes import PromptAttributes
from .handlers import FILE_HANDLERS

logger = logging.getLogger(__name__)

@dataclass
class PromptTemplate(BaseModel):
    type: str
    subtype: str
    prompt_text: str
    prompt_system_use: bool = False
    prompt_system_text: str = "You are a helpful AI Assistant"
    custom_system_prompt_name: Optional[str] = None
    notes: Optional[str] = None
    default_attributes: PromptAttributes = field(default_factory=PromptAttributes)

    def __post_init__(self):
        if isinstance(self.default_attributes, dict):
            logger.debug("PromptTemplate: converting default_attributes from dict.")
            self.default_attributes = PromptAttributes.from_dict(self.default_attributes)

    def get_placeholders(self) -> list[str]:
        return re.findall(r'<<\s*([\w.-]+)\s*>>', self.prompt_text)

    def get_file_placeholders(self) -> list[str]:
        return re.findall(r'%%\s*(.*?)\s*%%', self.prompt_text)

    def get_formatted_prompt(self, values: Dict[str, str | Path]) -> str:
        formatted = self.prompt_text
        missing = []

        for key in self.get_placeholders():
            if key in values and isinstance(values[key], str):
                formatted = re.sub(fr'<<\s*{re.escape(key)}\s*>>', values[key], formatted)
            else:
                missing.append(f"<< {key} >>")

        for key in self.get_file_placeholders():
            file_content = None
            val = values.get(key)

            if isinstance(val, str):
                val = Path(val)

            if isinstance(val, Path):
                handler = FILE_HANDLERS.get(val.suffix.lower())
                if handler:
                    try:
                        file_content = handler(val)
                    except Exception as e:
                        logger.error(f"Error in handler for {val}: {e}")
                        file_content = f"[Error reading file: {val.name}]"
                else:
                    file_content = f"[Unsupported file type: {val.suffix}]"
            elif isinstance(val, str):
                file_content = val

            if file_content is not None:
                formatted = formatted.replace(f"%% {key} %%", file_content)
            else:
                missing.append(f"%% {key} %%")

        if missing:
            logger.warning(f"Missing placeholders: {missing}")
        return formatted

    def get_original_prompt_hash(self) -> str:
        return hashlib.sha256(self.prompt_text.encode('utf-8')).hexdigest()

    def generate_prompt(self, prompt_text: str) -> list[str]:
        self.prompt_text = prompt_text
        return self.get_placeholders()

    def load_file_values(self, file_path: Path) -> Dict[str, str]:
        file_values = {}
        name = file_path.stem
        if file_path.exists() and file_path.is_file():
            with file_path.open("r", encoding="utf-8") as f:
                file_values[name] = f.read().strip()
        else:
            file_values[name] = f"[ERROR: {file_path.name} not found]"
        return file_values
