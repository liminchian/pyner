from datetime import datetime

import libxml2
import requests
from bs4 import BeautifulSoup


class Parser:
    def __init__(self, html: str):
        self._html = html

    def css_selector(self, selector: str) -> list:
        return BeautifulSoup(self._html, "html.parser").select(selector)

    def tag_and_class_finder(self, tag_name: str, attr=None):
        return BeautifulSoup(self._html, "html.parser").find_all(tag_name, attr)

    def xpath(self, expr: str):
        return libxml2.parseDoc(self._html).xpathEval(expr)


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
    root_page = "https://www.ptt.cc/bbs"
    default_page = "index.html"

    def __init__(self):
        self._urls = []
        self._seens = []
        self._headers = {"over18": "1"}
        self._board_list = list(
            map(
                lambda t: t.string,
                Parser(
                    Crawler(
                        url=f"{self.root_page}/{self.default_page}",
                        method="GET",
                        headers=self._headers,
                    ).response()
                ).tag_and_class_finder("div", ".board_name"),
            )
        )

    def get_articles(self, board_name: str) -> "Ptt":
        if board_name not in self._board_list:
            raise KeyError(f'couldn\'t find "{board_name}" in list.')
        else:
            self._urls = list(
                map(
                    lambda tag: tag["href"],
                    Parser(
                        Crawler(
                            url=f"{self.root_page}/{board_name}/{self.default_page}",
                            method="GET",
                            headers=self._headers,
                        ).response(),
                    ).css_selector("div.title > a"),
                )
            )

        return self


if __name__ == "__main__":
    pass
