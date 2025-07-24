from typing import List


class Message:
    def __init__(self, role: str, content: str) -> None:
        self.role: str = role
        self.content: str = content

    @property
    def role(self) -> str:
        return self._role

    @role.setter
    def role(self, role: str) -> None:
        self._role = role

    @property
    def content(self) -> str:
        return self._content

    @content.setter
    def content(self, content: str) -> None:
        self._content = content

    def to_dict(self) -> dict:
        return {"role": self.role, "content": self.content}


Chat = List[Message]

