# tests/test_data_processor.py
import os

from crawler.model import ResponseModel
from data.processor import DataProcessor
from data.loader import TextLoader


def test_clean_text():
    loader = TextLoader()
    loader.load([
        ResponseModel(tag='test1', response="content1\nmessage1\n")
    ])
    loader.add(ResponseModel(tag='test2', response="content2\nmessage2\n"))
    processor = DataProcessor(loader)
    assert processor.text.save_txt(filename="test.txt") == True
    with open("test.txt", "r") as f:
        assert f.read() == "\n# test1\ncontent1\n    message1\n\n# test2\ncontent2\n    message2\n"
    os.remove("test.txt")
