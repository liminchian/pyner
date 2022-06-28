import libxml2
import requests
from bs4 import BeautifulStoneSoup


def parse(func):
    def inner(obj, *args, **kwargs):
        return func(obj, *args, **kwargs)

    return inner


# Web selector and find element by html string.
css_selector = parse(BeautifulStoneSoup.select)
xpath_selector = parse(libxml2.xpathContext.xpathEval)
tag = parse(BeautifulStoneSoup.find_all)

# Build html document.
xpath_parser = parse(libxml2.parseDoc)
soup = parse(BeautifulStoneSoup)


class Crawler(object):
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
