from abc import ABC, abstractmethod


class BaseStorage(ABC):

    @abstractmethod
    def create(self, key: str, record: dict) -> None:
        ...

    @abstractmethod
    def read(self, key: str) -> dict | None:
        ...

    @abstractmethod
    def read_all(self) -> list[dict]:
        ...

    @abstractmethod
    def update(self, key: str, record: dict) -> bool:
        ...

    @abstractmethod
    def delete(self, key: str) -> bool:
        ...
