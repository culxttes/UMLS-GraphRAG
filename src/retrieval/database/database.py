from abc import ABC, abstractmethod


class Database(ABC):
    @abstractmethod
    def query(self, query: str) -> str: ...
