from typing import Generic, TypeVar

from storages.base import BaseStorage

RecordType = TypeVar('RecordType')


class InMemoryStorage(BaseStorage[RecordType], Generic[RecordType]):

    def __init__(self) -> None:
        self._storage: dict[str, RecordType] = {}

    def create(self, key: str, record: RecordType) -> None:
        self._storage[key] = record

    def read(self, key: str) -> RecordType | None:
        return self._storage.get(key)

    def read_all(self) -> list[RecordType]:
        return list(self._storage.values())

    def update(self, key: str, record: RecordType) -> bool:
        if key not in self._storage:
            return False
        self._storage[key] = record
        return True

    def delete(self, key: str) -> bool:
        if key not in self._storage:
            return False
        self._storage.pop(key)
        return True
