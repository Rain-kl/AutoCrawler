# tests/test_data_processor.py
from crawler.model import ResponseModel
from data.processor import DataProcessor
from data.loader import TextLoader


def test_clean_text():
    loader = TextLoader()
    loader.load([
        ResponseModel(tag='test', response="asjdkh\nsdadsasdasd\n")
    ])
    processor = DataProcessor(loader)
    assert processor.text.save_txt(filename="test.txt") == True

