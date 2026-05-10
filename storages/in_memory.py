from storages.base import BaseStorage


class InMemoryStorage(BaseStorage):

    def __init__(self) -> None:
        self._storage: dict = {}

    def create(self, key: str, record: dict) -> None:
        self._storage[key] = record

    def read(self, key: str) -> dict | None:
        return self._storage.get(key)

    def read_all(self) -> list[dict]:
        return list(self._storage.values())

    def update(self, key: str, record: dict) -> bool:
        if key not in self._storage:
            return False
        self._storage[key] = record
        return True

    def delete(self, key: str) -> bool:
        if key not in self._storage:
            return False
        self._storage.pop(key)
        return True
