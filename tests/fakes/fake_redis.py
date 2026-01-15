class FakeRedis:
    def __init__(self):
        self._store = {}

    def exists(self, key: str) -> bool:
        return key in self._store

    def setex(self, name: str, time: int, value: str):
        # ignoramos TTL nos testes
        self._store[name] = value

    def get(self, key: str):
        return self._store.get(key)

    def delete(self, key: str):
        self._store.pop(key, None)
