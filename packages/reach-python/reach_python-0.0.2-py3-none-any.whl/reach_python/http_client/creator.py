from abc import abstractmethod, ABC


class HTTPClient(ABC):
    @abstractmethod
    def post(self, url: str, data: dict = None) -> dict:
        pass

