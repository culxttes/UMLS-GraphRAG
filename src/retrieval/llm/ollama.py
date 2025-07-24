from typing import Optional, Callable
from ollama import Client, ChatResponse
from .llm import LLM
from .chat import Chat


class Ollama(LLM):
    def __init__(
        self,
        host: Optional[str],
        model: str,
        chat: Chat = list(),
        cleaner: Optional[Callable[[str], str]] = None,
        **kwargs,
    ) -> None:
        self._client: Client = Client(host, **kwargs)
        self._model: str = model
        self._chat: Chat = chat
        self._cleaner: Optional[Callable[[str], str]] = cleaner

    def chat(self, chat: Chat = list()) -> str:
        chat = self._chat + chat
        response: ChatResponse = self._client.chat(
            model=self._model, messages=[message.to_dict() for message in chat]
        )
        if self._cleaner is not None:
            return self._cleaner(response.message.content)
        return response.message.content
