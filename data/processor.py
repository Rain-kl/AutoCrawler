# data/processor.py
import json
from typing import Union

from .loader import DataLoader, TextLoader


def AutoProcessor(loader: Union[DataLoader, TextLoader]):
    if isinstance(loader, TextLoader):
        return TextProcessor(loader)
    elif isinstance(loader, DataLoader):
        return DataProcessor(loader)
    else:
        raise ValueError("Loader type not supported")


class DataProcessor:
    def __init__(self, loader: Union[DataLoader, TextLoader]):
        self.loader = loader


class TextProcessor:
    def __init__(self, loader: TextLoader):
        self.loader = loader
        assert self.loader.data is not None, "Loader is not loaded"

    def save_txt(self, filename="save.txt", tag_prefix="#") -> bool:
        with open(filename, "w") as f:
            for tag, response in self.loader:
                tag_line = "\n" + f"{tag_prefix} {tag}".strip() + "\n"
                f.write(tag_line)
                f.write("\n    ".join(response))
                f.write("\n")
        return True

    def save_json(self, filename="save.json") -> bool:
        json_data = []
        with open(filename, "w") as f:
            for tag, response in self.loader:
                json_data.append({
                    "tag": tag,
                    "response": response
                })
            json.dump(json_data, f, ensure_ascii=False, indent=4)
        return True
