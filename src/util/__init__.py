"""
This module aggregates utility functions for file reading, string unwrapping,
, cleaner string and template-based prompt generation.
"""

from .read_to_string import read_to_string
from .unwrap import unwrap
from .cleaner import strip_code_fences
from .user_prompt import user_prompt
from .generator_system_prompt import generator_system_prompt


__all__: list[str] = [
    "read_to_string",
    "unwrap",
    "user_prompt",
    "generator_system_prompt",
]
