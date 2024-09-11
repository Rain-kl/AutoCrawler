# tests/test_parser.py

from crawler.parser import Parser


def test_parse_html():
    html_content = "<html><head><title>Test Page</title></head><body><p>Hello, world!</p></body></html>"

    parser = Parser(html_content,type_='text')
    target = parser.html.find('p')
    print(target)
    assert target[0].text== "Hello, world!"


def test_extract_links():
    html_content = '<html><body><a href="http://example.com">Example</a></body></html>'
    parser = Parser(html_content,type_='text')
    target = parser.html.find('a')

    assert target[0].attributes['href'] == "http://example.com"