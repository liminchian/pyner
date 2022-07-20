from pyner import crawler


def test_Parser_css_selector_():
    html = '<html><a class="title">Success</a></html>'
    assert (
        list(crawler.Parser(html).css_selector("a.title").map(lambda tag: tag.string))[
            0
        ]
        == "Success"
    )

    html = '<html><a href="http://test">Success</a></html>'
    assert (
        list(crawler.Parser(html).css_selector("a.title").map(lambda tag: tag["href"]))[
            0
        ]
        == "http://test"
    )
