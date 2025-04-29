from typing import Optional, Dict, Type
from src.kv.inter import Kv
from src.kv.impl_dict import DictKv


class KvFactory:
    """
    Factory class for creating key-value database instances.
    Provides methods to create different implementations of the Kv interface.
    """

    # Registry of available KV implementations
    _implementations: Dict[str, Type[Kv]] = {"dict": DictKv}

    @classmethod
    def create(cls, impl: str, **kwargs) -> Optional[Kv]:
        """
        Create a new instance of a Kv implementation.

        Args:
            implementation (str): The name of the implementation to create
            **kwargs: Additional arguments to pass to the implementation constructor

        Returns:
            Optional[Kv]: A new instance of the requested Kv implementation,
                         or None if the implementation is not found
        """
        if impl not in cls._implementations:
            return None

        return cls._implementations[impl](**kwargs)

    @classmethod
    def register_implementation(cls, name: str, implementation: Type[Kv]) -> None:
        """
        Register a new Kv implementation.

        Args:
            name (str): The name to register the implementation under
            implementation (Type[Kv]): The implementation class to register
        """
        cls._implementations[name] = implementation

    @classmethod
    def get_available_implementations(cls) -> list[str]:
        """
        Get a list of available Kv implementations.

        Returns:
            list[str]: A list of names of available implementations
        """
        return list(cls._implementations.keys())
