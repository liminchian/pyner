import re
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from itertools import chain
from typing import Any, Callable, Dict, Iterable, Iterator

import requests
from bs4 import BeautifulSoup, Tag


@dataclass
class Articles:
    html: str
    kwds: Dict[str, Callable] = field(default_factory=Dict[str, Callable])

    def __post_init__(self) -> None:
        for name, func in self.kwds.items():
            setattr(self, name, func(self.html))


class Parser:
    def __init__(self, html: str):
        self._html = html
        self._data: Iterable[Any] = []

    def css_selector(self, selector: str):
        self._data = chain(BeautifulSoup(self._html, "html.parser").select(selector))
        return self

    def tag_and_class_finder(self, tag_name: str, attr=None):
        self._data = chain(
            BeautifulSoup(self._html, "html.parser").find_all(tag_name, attr)
        )
        return self

    def xpath(self, expr: str):
        self._data = chain(ET.fromstring(self._html).findall(expr))
        return self

    def rex(self, pattern: str):
        self._data = chain(re.findall(pattern, self._html))
        return self

    @property
    def data(self):
        return self._data

    def map(self, func):
        return map(func, self._data)


def response(url: str, method="GET", headers={}, data={}, proxies={}):
    with requests.Session() as rs:
        return rs.request(
            url=url,
            method=method,
            headers=headers,
            params=data,
            proxies=proxies,
        )
