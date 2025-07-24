"""
This module exposes the public interface for the LLM components, including:

- Message: Represents a single chat message.
- Chat: A list of Message instances forming a conversation.
- LLM: Abstract base class for language models.
- Ollama: Concrete implementation of LLM using the Ollama API.
"""

from .chat import Message, Chat
from .llm import LLM
from .ollama import Ollama


__all__: list[str] = ["Message", "Chat", "LLM", "Ollama"]
