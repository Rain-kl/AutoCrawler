# data/data_processor.py

class DataProcessor:
    def clean_text(self, text: str) -> str:
        """
        Clean text data by removing unnecessary whitespace and special characters.
        """
        cleaned_text = text.strip().replace("\n", " ").replace("\r", "")
        return cleaned_text

    def extract_information(self, raw_data: dict) -> dict:
        """
        Extract relevant information from raw data.
        """
        extracted_data = {
            "title": self.clean_text(raw_data.get("title", "")),
            "author": self.clean_text(raw_data.get("author", "")),
            "content": self.clean_text(raw_data.get("content", "")),
        }
        return extracted_data

# 实例化全局数据处理器
data_processor = DataProcessor()

# 在项目中使用 DataProcessor
raw_sample_data = {
    "title": " Example Title  ",
    "author": " Example Author ",
    "content": " Example Content\nwith line breaks. "
}

processed_data = data_processor.extract_information(raw_sample_data)
print(processed_data)  # {'title': 'Example Title', 'author': 'Example Author', 'content': 'Example Content with line breaks.'}