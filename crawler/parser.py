# crawler/parser.py

from bs4 import BeautifulSoup


class Parser:
    @staticmethod
    def parse_html(html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        return soup

    @staticmethod
    def extract_links(soup):
        return [a['href'] for a in soup.find_all('a', href=True)]


# 在项目中使用 Parser
parser = Parser()
