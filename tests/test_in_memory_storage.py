from storages.in_memory import InMemoryStorage


class TestInMemoryStorage:

    def test_create_and_read_ok(self, storage: InMemoryStorage) -> None:
        storage.create("alice", {"name": "Alice"})

        assert storage.read("alice") == {"name": "Alice"}

    def test_read_no_data_ok(self, storage: InMemoryStorage) -> None:
        assert storage.read("bla bla bla") is None

    def test_read_all_ok(self, storage: InMemoryStorage) -> None:
        storage.create("alice", {"name": "Alice"})
        storage.create("bob", {"name": "Bob"})

        assert storage.read_all() == [{"name": "Alice"}, {"name": "Bob"}]

    def test_update_ok(self, storage: InMemoryStorage) -> None:
        storage.create("alice", {"name": "Alice"})

        assert storage.update("alice", {"name": "Alice Updated"}) is True
        assert storage.read("alice") == {"name": "Alice Updated"}

    def test_delete_ok(self, storage: InMemoryStorage) -> None:
        storage.create("alice", {"name": "Alice"})

        assert storage.delete("alice") is True
        assert storage.read("alice") is None
