import json
from typing import ContextManager, Generator, List


class Pipe:
    @classmethod
    def from_json(cls, fp: str):
        raise NotImplemented

    def run(self) -> Generator:
        raise NotImplemented

    def __str__(self) -> str:
        return f"{self.__class__} at {hex(id(self))}"


class Pipeline(ContextManager):
    def __init__(self):
        self._content: List[Pipe] = []

    def add(self, pipe: Pipe):
        self._content.append(pipe)

    def run(self):
        pass

    def __str__(self) -> str:
        return f"{self.__class__} at {hex(id(self))}"

    def __getitem__(self, index: int) -> Pipe:
        return self._content[index]

    def __len__(self) -> int:
        return len(self._content)
