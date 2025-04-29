from abc import ABC, abstractmethod
from typing import Any, Optional


class Kv(ABC):
    """
    Interface for key-value database operations.
    Provides methods for retrieving, storing, and deleting key-value pairs.
    """

    @abstractmethod
    async def get(self, key: str) -> Optional[Any]:
        """
        Retrieve a value by its key.

        Args:
            key (str): The key to retrieve the value for

        Returns:
            Optional[Any]: The value if found, None otherwise
        """
        pass

    @abstractmethod
    async def put(self, key: str, value: Any) -> bool:
        """
        Store a key-value pair.

        Args:
            key (str): The key to store
            value (Any): The value to store

        Returns:
            bool: True if storage was successful, False otherwise
        """
        pass

    @abstractmethod
    async def zap(self, key: str) -> bool:
        """
        Delete a key-value pair by its key.

        Args:
            key (str): The key to delete

        Returns:
            bool: True if deletion was successful, False otherwise
        """
        pass
