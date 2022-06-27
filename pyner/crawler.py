import libxml2
import requests
from bs4 import BeautifulStoneSoup


def response(headers=None, body=None):
    def inner(url: str, method: str):
        with requests.Session() as rs:
            return rs.request(method, url, headers=headers, data=body).text

    return inner


def selector(func):
    def inner(html, *args, **kwargs):
        return func(html, *args, **kwargs)

    return inner


css_selector = selector(BeautifulStoneSoup.select)
tag_selector = selector(BeautifulStoneSoup.find_all)
xpath_selector = selector(libxml2.xpathContext.xpathEval)
