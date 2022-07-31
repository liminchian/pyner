import re
import xml.etree.ElementTree as ET
from itertools import chain
from typing import Any, Iterable, List

import requests
from bs4 import BeautifulSoup


class Articles:
    def __init__(self, html: str, **kwargs) -> None:
        self.html = html
        self.kwargs = kwargs
        for name, func in kwargs.items():
            if hasattr(func, "__call__"):
                setattr(self, name, func(self.html))
            else:
                setattr(self, name, func)

    def to_dict(self) -> dict:
        return {name: getattr(self, name) for name in self.kwargs.keys()}

    def __str__(self) -> str:
        return self.to_dict().__str__()


class Parser:
    def __init__(self, html: str):
        self._html = html
        self._data: Iterable[Any] = []
        self._chain = lambda it: chain(it) if isinstance(it, Iterable) else it

    def css_selector(self, selector: str):
        self._data = self._chain(
            BeautifulSoup(self._html, "html.parser").select(selector)
        )
        return self

    def tag_and_class_finder(self, tag_name: str, attr=None):
        self._data = self._chain(
            BeautifulSoup(self._html, "html.parser").find_all(tag_name, attr)
        )
        return self

    def xpath(self, expr: str):
        self._data = self._chain(ET.fromstring(self._html).findall(expr))
        return self

    def rex(self, pattern: str):
        self._data = self._chain(re.findall(pattern, self._html))
        return self

    @property
    def data(self) -> List[Any]:
        return list(self._data)

    def map(self, func):
        self._data = self._chain(map(func, self._data))
        return self


def response(url: str, method="GET", headers={}, data={}, proxies={}):
    with requests.Session() as rs:
        return rs.request(
            url=url,
            method=method,
            headers=headers,
            params=data,
            proxies=proxies,
        )
