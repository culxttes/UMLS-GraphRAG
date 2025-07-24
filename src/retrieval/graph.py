from .llm import LLM
from .llm.chat import Chat
from .database import Database


class Graph(LLM):
    def __init__(self, llm: LLM, database: Database) -> None:
        self._llm: LLM = llm
        self._database: Database = database

    def chat(self, chat: Chat = list()) -> str:
        query: str = self._llm.chat(chat)

        print(f"[DEBUG] Request:\n{query}")

        result: str = self._database.query(query)

        return result
