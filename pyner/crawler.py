from datetime import datetime
from typing import Dict, Iterable, List

import libxml2
import requests
from bs4 import BeautifulSoup

from pyner.utils import _Pipe, watch


def get_html(
    url: str,
    method: str,
    headers=None,
    data=None,
    proxies=None,
):
    with requests.Session() as rs:
        return rs.request(
            url=url,
            method=method,
            headers=headers,
            params=data,
            proxies=proxies,
        ).text


class Parser(_Pipe):
    def __init__(self, html: str):
        self._html = html

    @watch
    def css_selector(self, selector: str) -> list:
        return BeautifulSoup(self._html, "html.parser").select(selector)

    @watch
    def tag_and_class_finder(self, tag_name: str, attr=None):
        return BeautifulSoup(self._html, "html.parser").find_all(tag_name, attr)

    @watch
    def xpath(self, expr: str):
        return libxml2.parseDoc(self._html).xpathEval(expr)


class Crawler(_Pipe):
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

    @watch
    def response(self) -> Parser:
        return Parser(
            get_html(
                method=self._method,
                url=self._url,
                headers=self._headers,
                data=self._body,
                proxies=self._proxies,
            )
        )


class Article(_Pipe):
    def __init__(
        self,
        url: str,
        headers=None,
        body=None,
        proxies=None,
    ) -> None:
        self._data = {}
        self._url = url
        self._parser = Crawler(
            url,
            method="GET",
            headers=headers,
            body=body,
            proxies=proxies,
        ).response()

    @watch
    def add_column(
        self,
        name: str,
        *,
        xpath=None,
        css_selector=None,
        tag=None,
        attr=None,
    ):
        if xpath:
            self._data[name] = self._parser.xpath(xpath)
        elif css_selector:
            self._data[name] = self._parser.css_selector(css_selector)
        elif tag:
            if attr:
                self._data[name] = self._parser.tag_and_class_finder(tag)
            else:
                self._data[name] = self._parser.tag_and_class_finder(tag, attr=attr)
        else:
            raise RuntimeError("No parameters get.")

    def __get_data(self):
        self._data["page"] = self._url
        return self._data

    data = property(__get_data)


class Ptt(_Pipe):
    root_page = "https://www.ptt.cc/bbs"
    default_page = "index.html"

    def __init__(self) -> None:
        self._data = []
        self._seens = []
        self._headers = {"over18": "1"}
        self._board_list = list(
            map(
                lambda t: t.string,
                Crawler(
                    url=f"{self.root_page}/{self.default_page}",
                    method="GET",
                    headers=self._headers,
                )
                .response()
                .tag_and_class_finder("div", ".board_name"),
            )
        )

    @watch
    def get_links(self, board_name: str) -> Iterable[str]:
        if board_name not in self._board_list:
            raise KeyError(f'couldn\'t find "{board_name}" in list.')
        return map(
            lambda tag: tag["href"].string,
            Crawler(
                url=f"{self.root_page}/{board_name}/{self.default_page}",
                method="GET",
            )
            .response()
            .css_selector("div.title > a"),
        )


if __name__ == "__main__":
    pass
