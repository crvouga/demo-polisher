from typing import Any, Dict, Optional
from src.kv.inter import Kv


class DictKv(Kv):
    """
    In-memory implementation of the Kv interface using a Python dictionary.
    This implementation stores all key-value pairs in memory and is not persistent.
    """

    def __init__(self):
        """Initialize an empty dictionary for storage."""
        self._storage: Dict[str, Any] = {}

    async def get(self, key: str) -> Optional[Any]:
        """
        Retrieve a value by its key.

        Args:
            key (str): The key to retrieve the value for

        Returns:
            Optional[Any]: The value if found, None otherwise
        """
        return self._storage.get(key)

    async def put(self, key: str, value: Any) -> bool:
        """
        Store a key-value pair.

        Args:
            key (str): The key to store
            value (Any): The value to store

        Returns:
            bool: True if storage was successful, False otherwise
        """
        try:
            self._storage[key] = value
            return True
        except Exception:
            return False

    async def zap(self, key: str) -> bool:
        """
        Delete a key-value pair by its key.

        Args:
            key (str): The key to delete

        Returns:
            bool: True if deletion was successful, False otherwise
        """
        if key in self._storage:
            del self._storage[key]
            return True
        return False
