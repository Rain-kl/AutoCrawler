# plugins/text_extractor.py

from bs4 import BeautifulSoup
from plugins import BaseExtractor

class TextExtractor(BaseExtractor):
    def extract(self, content: str) -> dict:
        soup = BeautifulSoup(content, 'html.parser')
        extracted_data = {
            "title": soup.title.string if soup.title else None,
            "body_text": soup.get_text()
        }
        return extracted_data

def get_plugin():
    return TextExtractor()