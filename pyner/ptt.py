import re
from datetime import datetime
from typing import Iterable, List

from pyner.crawler import Articles, Parser, response


class Ptt:
    main_page = "index.html"
    default_domain = "https://www.ptt.cc"
    headers = {
        "Cookie": "over18=1",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0",
    }

    def __init__(self, block: str) -> None:
        self._block = f"bbs/{block}"
        self._page_rex = lambda link: re.compile(
            r"^/\w+/\w+/index(?P<page>\d+)\.html$"
        ).match(link)
        self._url = f"{self.default_domain}/{self._block}/{self.main_page}"
        self._response = response(self._url, headers=self.headers)
        self._seen_urls: List[str] = []
        self._articles: List[Articles] = list(self._get_articles())

    def _switch_page(self, page: int):
        name, suffix = self.main_page.rsplit(".")
        self._seen_urls.append(self._response.text)
        self._url = f"{self.default_domain}/{self._block}/{name}{page}.{suffix}"

    def _get_page(self) -> int:
        m = self._page_rex(
            list(
                Parser(self._response.text)
                .css_selector("div.btn-group:nth-child(2) > a:nth-child(2)")
                .map(lambda tag: tag["href"])
            )[0]
        )
        if m:
            return int(m.group("page")) + 1
        else:
            raise RuntimeError("can not find page.")

    def _get_articles(self) -> Iterable[Articles]:
        links = (
            Parser(self._response.text)
            .css_selector("div.title > a")
            .map(lambda tag: self.default_domain + tag["href"])
        )
        kwds = {
            "title": lambda html: Parser(html)
            .css_selector("div.article-metaline:nth-child(3) > span:nth-child(2)")
            .map(lambda tag: tag.string),
            "create_time": lambda html: Parser(html)
            .css_selector("div.article-metaline:nth-child(4) > span:nth-child(2)")
            .map(lambda tag: datetime.strptime(tag.string, "%a %b %d %H:%M:%S %Y")),
        }
        for link in links:
            art = Articles(response(link, headers=self.headers).text, kwds)
            yield art

    @property
    def page_number(self) -> int:
        return self._get_page()

    @page_number.setter
    def page_number(self, page: int):
        self._switch_page(page)

    @property
    def articles(self) -> int:
        return len(self._articles)

    def __str__(self) -> str:
        return f"<[{self._response.status_code}] domain: {self._block}, have {self.articles} articles at No.{self.page_number} page>"


if __name__ == "__main__":
    print(Ptt("Gossiping"))
