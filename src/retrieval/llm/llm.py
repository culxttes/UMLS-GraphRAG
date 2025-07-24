from abc import ABC, abstractmethod
from .chat import Chat


class LLM(ABC):
    @abstractmethod
    def chat(self, chat: Chat) -> str: ...
