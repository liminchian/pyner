from pyner import crawler


def test_Parser_css_selector_():
    html = '<html><a class="title">Success</a></html>'
    assert crawler.Parser(html).css_selector("a.title").map(
        lambda tag: tag.string
    ).data == ["Success"]

    html = '<html><a class="title" href="http://test">Success</a></html>'
    assert crawler.Parser(html).css_selector("a.title").map(
        lambda tag: tag["href"]
    ).data == ["http://test"]
