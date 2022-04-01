import urllib
from typing import Iterator, List

import numpy as np

from pyner.utils.decorator import logger


class Pipe(Iterator):
    def __init__(self, input_data: np.Arrayterator):
        self._input_data = input_data

    def __str__(self) -> str:
        return f"{self.__class__} at {hex(id(self))}"

    @logger
    def __iter__(self):
        pass

    def run(self):
        raise NotImplemented


class Pipeline(object):
    def __init__(self):
        self._content: List[Pipe] = []

    def add(self, pipe: Pipe):
        self._content.append(pipe)

    def __str__(self) -> str:
        return f"{self.__class__} at {hex(id(self))}"

    def __getitem__(self, index: int) -> Pipe:
        return self._content[index]

    def __len__(self) -> int:
        return len()


class Req(Pipe):
    pass


class Selector(Pipe):
    pass


class DataCollector(Pipe):
    pass
