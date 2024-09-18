from abc import ABC, abstractmethod
from typing import Iterator, Tuple, List

from crawler.model import ResponseModel


class DataLoader(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def __iter__(self):
        raise NotImplementedError

    @abstractmethod
    def load(self, data: list[ResponseModel]):
        """
        加载Loader时调用
        """
        raise NotImplementedError

    @abstractmethod
    def add(self, data: ResponseModel):
        """
        添加数据
        """
        raise NotImplementedError

    @abstractmethod
    def empty(self):
        """
        清空数据
        """
        raise NotImplementedError

    @abstractmethod
    def process_response(self, data: List[ResponseModel]) -> List[ResponseModel]:
        """
        处理数据response部分
        存在默认，也可以由用户自行实现
        """
        raise NotImplementedError


class TextLoader(DataLoader):

    def __init__(self, ):
        super().__init__()
        self.data: List[ResponseModel] = []

    def load(self, data: List[ResponseModel]):
        """
        加载Loader时调用
        """
        for item in data:
            self.add(item)

    def add(self, data: ResponseModel):
        """
        添加数据
        """
        self.data.append(self.process_response(data))

    def empty(self):
        self.data = []

    def process_response(self, data: ResponseModel) -> ResponseModel:
        """
        默认实现，可以由用户自行实现
        """
        response = data.response.split('\n')
        response = [i.strip() for i in response if i.strip()]
        return ResponseModel(tag=data.tag, response=response)

    def __iter__(self) -> Iterator[Tuple[str, List[str]]]:
        for item in self.data:
            yield item.tag, item.response
