# data/processor.py
from .loader import DataLoader


class DataProcessor:
    def __init__(self, loader: DataLoader):
        self.loader = loader
        self.text = TextProcessor(loader)


class TextProcessor:
    def __init__(self, loader: DataLoader):
        self.loader = loader

    def save_text(self):
        pass
