from abc import ABC, abstractmethod
from typing import Generic, TypeVar

RecordType = TypeVar('RecordType')


class BaseStorage(ABC, Generic[RecordType]):

    @abstractmethod
    def create(self, key: str, record: RecordType) -> None:
        ...

    @abstractmethod
    def read(self, key: str) -> RecordType | None:
        ...

    @abstractmethod
    def read_all(self) -> list[RecordType]:
        ...

    @abstractmethod
    def update(self, key: str, record: RecordType) -> bool:
        ...

    @abstractmethod
    def delete(self, key: str) -> bool:
        ...
