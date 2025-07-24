"""
This module defines the OpenAI class, a concrete implementation of the LLM interface,
which uses the OpenAI API to generate responses from a chat history.
"""

from typing import Optional, Callable
from openai.types.chat import ChatCompletion
import openai
from .llm import LLM
from .chat import Chat


class OpenAI(LLM):
    """
    An implementation of the LLM interface using the OpenAI API.

    This class manages an ongoing chat session with a specified model,
    and optionally allows post-processing of the response using a cleaner function.
    """

    def __init__(
        self,
        host: Optional[str],
        api_key: str,
        model: str,
        chat: Chat = list(),
        cleaner: Optional[Callable[[str], str]] = None,
    ) -> None:
        """
        Initializes the OpenAI LLM client.

        Parameters:
        - host (Optional[str]): The host URL for the OpenAI server. If None, defaults are used.
        - api_key (str): The API key used to authenticate requests to the OpenAI server.
        - model (str): The name of the model to use (e.g., "llama3").
        - chat (Chat, optional): Initial list of messages to include in the chat history. Defaults to an empty list.
        - cleaner (Optional[Callable[[str], str]]): A function to post-process the model's response.
        """

        self._client: openai.OpenAI = openai.OpenAI(base_url=host, api_key=api_key)
        self._model: str = model
        self._chat: Chat = chat
        self._cleaner: Optional[Callable[[str], str]] = cleaner

    def chat(self, chat: Chat = list()) -> str:
        chat = self._chat + chat
        response: ChatCompletion = self._client.chat.completions.create(
            model=self._model, messages=[message.to_dict() for message in chat]
        )
        if self._cleaner is not None:
            return self._cleaner(response.choices[0].message.content)
        return response.choices[0].message.content
