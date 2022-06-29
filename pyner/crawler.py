from datetime import datetime
from enum import Enum

import libxml2
import requests
from bs4 import BeautifulStoneSoup


class ParseOption(Enum):
    ClassAndTag = ("ClassAndTag", BeautifulStoneSoup, BeautifulStoneSoup.find_all)
    Css = ("Css", BeautifulStoneSoup, BeautifulStoneSoup.select)
    Xpath = ("Xpath", libxml2.parseDoc, libxml2.xpathContext.xpathEval)

    def __new__(cls, name, parser, method) -> "ParseOption":
        parse = object.__new__(cls)
        setattr(parse, "name", name)
        setattr(parse, "parser", parser)
        setattr(parse, "method", method)
        return parse


class Crawler:
    def __init__(
        self,
        url: str,
        method: str,
        headers=None,
        body=None,
        proxies=None,
    ) -> None:
        self._url = url
        self._method = method
        self._headers = headers
        self._body = body
        self._proxies = proxies

    def response(self) -> str:
        with requests.Session() as rs:
            return rs.request(
                method=self._method,
                url=self._url,
                headers=self._headers,
                data=self._body,
                proxies=self._proxies,
            ).text


class Ptt:
    root_page = "https://www.ptt.cc/bbs/index.html"

    def __init__(self):
        self._html = Crawler(url=self.root_page, method="GET")
