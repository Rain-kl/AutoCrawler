# tests/test_data_processor.py

from data.data_processor import DataProcessor


def test_clean_text():
    processor = DataProcessor()
    dirty_text = " Example Text  "
    cleaned_text = processor.clean_text(dirty_text)

    assert cleaned_text == "Example Text"


def test_extract_information():
    processor = DataProcessor()
    raw_data = {
        "title": " Example Title  ",
        "author": " Example Author ",
        "content": " Example Content\nwith line breaks. "
    }
    extracted_data = processor.extract_information(raw_data)

    assert extracted_data == {
        "title": "Example Title",
        "author": "Example Author",
        "content": "Example Content with line breaks."
    }