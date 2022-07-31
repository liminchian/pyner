import re
from datetime import datetime
from typing import Any, Dict, Iterable, List, Set

from pyner.crawler import Articles, Parser, response
from pyner.utils import watch


class Ptt:
    main_page = "index.html"
    default_domain = "https://www.ptt.cc"
    headers = {
        "Cookie": "over18=1",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0",
    }

    def __init__(self, block: str) -> None:
        self._block = f"bbs/{block}"
        self._get_link = (
            lambda tag: self.default_domain + tag["href"]
            if self._block in tag["href"]
            else self.default_domain + self._block + tag["href"]
        )
        self._get_response = lambda url: response(url, headers=self.headers)
        self._link_parser = (
            lambda response: Parser(response.text)
            .css_selector("div.title > a")
            .map(self._get_link)
            .data
        )
        self._page_parser = (
            lambda response: Parser(response.text)
            .css_selector("div.btn-group:nth-child(2) > a:nth-child(2)")
            .map(self._get_link)
            .data
        )
        self._get_page_number = (
            lambda link: int(re.compile(r"(\d+)").findall(link)[0]) + 1
            if re.compile(r"(\d+)").findall(link)[0]
            else 0
        )

        self._url = f"{self.default_domain}/{self._block}/{self.main_page}"
        self._response = self._get_response(self._url)
        self._max_page = self._get_page_number(self._page_parser(self._response)[0])
        self._task: List[str] = self._link_parser(self._response)
        self._seen_urls: Set[str] = set()

    def _get_comment_datetime(self, tag):
        # datetime format -> mm/dd hh:mm
        _, *dt = tag.string.split()
        return " ".join(dt)

    def _get_article_comment(self, html: str) -> Dict[str, Any]:
        return Articles(
            html,
            tag=lambda html: Parser(html)
            .css_selector("span.hl.push-tag")
            .map(lambda tag: tag.string)
            .data,
            userid=lambda html: Parser(html)
            .css_selector("span.f3.hl.push-userid")
            .map(lambda tag: tag.string)
            .data,
            content=lambda html: Parser(html)
            .css_selector("span.f3.push-content")
            .map(lambda tag: tag.string)
            .data,
            ip=lambda html: Parser(html)
            .css_selector("span.push-ipdatetime")
            .map(lambda tag: tag.string.split()[0] if tag else "")
            .data,
            datetime=lambda html: Parser(html)
            .css_selector("span.push-ipdatetime")
            .map(self._get_comment_datetime)
            .data,
        ).to_dict()

    def _switch_page(self, page: int):
        name, suffix = self.main_page.rsplit(".")
        self._seen_urls.add(self._url)
        if page > 0 and page <= self._max_page:
            self._url = f"{self.default_domain}/{self._block}/{name}{page}.{suffix}"
            self._response = self._get_response(self._url)
            self._task.extend(self._link_parser(self._response))

    @property
    def articles(self) -> Iterable[Articles]:
        for link in self._task:
            if link in self._seen_urls:
                continue
            else:
                self._seen_urls.add(link)
            yield Articles(
                self._get_response(link).text,
                title=lambda html: Parser(html)
                .css_selector("div.article-metaline:nth-child(3) > span:nth-child(2)")
                .map(lambda tag: tag.string)
                .data,
                create_time=lambda html: Parser(html)
                .css_selector("div.article-metaline:nth-child(4) > span:nth-child(2)")
                .map(lambda tag: datetime.strptime(tag.string, "%a %b %d %H:%M:%S %Y"))
                .data,
                comment=lambda html: Parser(html)
                .css_selector("div.push")
                .map(lambda tag: self._get_article_comment(str(tag)))
                .data,
            )

    @property
    def page(self):
        return self._get_page_number(self._page_parser(self._response)[0])

    @page.setter
    def page(self, number: int):
        self._switch_page(number)

    def __str__(self) -> str:
        return f"<[{self._response.status_code}] domain: {self._block}, have {len(self._task)} articles at No.{self.page} page>"


if __name__ == "__main__":
    gossiping = Ptt("Gossiping")
    gossiping.page -= 1
    print(gossiping)
