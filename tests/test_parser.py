# tests/test_parser.py

from crawler.parser import Parser


def test_parse_html():
    parser = Parser()
    html_content = "<html><head><title>Test Page</title></head><body><p>Hello, world!</p></body></html>"
    soup = parser.parse_html(html_content)

    assert soup.title.string == "Test Page"


def test_extract_links():
    parser = Parser()
    html_content = '<html><body><a href="http://example.com">Example</a></body></html>'
    soup = parser.parse_html(html_content)
    links = parser.extract_links(soup)

    assert links == ["http://example.com"]