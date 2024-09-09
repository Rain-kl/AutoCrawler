from typing import Iterator, Tuple, List

from crawler.model import ResponseModel


class DataLoader:
    def __init__(self):
        pass

    def __iter__(self):
        raise NotImplementedError

    def load(self, data: list[ResponseModel]):
        """
        加载Loader时调用
        """
        raise NotImplementedError

    def process_response(self, data: List[ResponseModel]) -> List[ResponseModel]:
        """
        处理数据response部分
        存在默认，也可以由用户自行实现
        """
        raise NotImplementedError


class TextLoader(DataLoader):
    def __init__(self, ):
        super().__init__()
        self.data = None

    def load(self, data: List[ResponseModel]):
        """
        加载Loader时调用
        """
        data_processed = self.process_response(data)
        self.data = data_processed

    def process_response(self, data: List[ResponseModel]) -> List[ResponseModel]:
        """
        默认实现，可以由用户自行实现
        """
        data_loader = []
        for i in data:
            response = i.response.split('\n')
            response = [i.strip() for i in response if i.strip()]
            data_loader.append(
                ResponseModel(tag=i.tag, response=response)
            )
        return data_loader

    def __iter__(self) -> Iterator[Tuple[str, List[str]]]:
        for item in self.data:
            yield item.tag, item.response
