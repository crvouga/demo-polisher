from typing import Dict, Type, Literal, Union
from src.object_storage.inter import ObjectStorage
from src.object_storage.impl_local import LocalObjectStorage


class ObjectStorageFactory:
    """
    Factory class for creating ObjectStorage instances.
    """

    _storage_types: Dict[str, Type[ObjectStorage]] = {
        "local": LocalObjectStorage,
    }

    @classmethod
    def create(cls, storage_type: Literal["local"], **kwargs) -> ObjectStorage:
        """
        Create an instance of the specified object storage.

        Args:
            storage_type (Literal["local"]): The type of storage to create
            **kwargs: Arguments to pass to the storage constructor
                      (e.g., base_dir for LocalObjectStorage)

        Returns:
            ObjectStorage: An instance of the requested storage

        Raises:
            ValueError: If the storage type is not supported
        """
        if storage_type not in cls._storage_types:
            raise ValueError(
                f"Unsupported storage type: {storage_type}. "
                f"Supported types are: {', '.join(cls._storage_types.keys())}"
            )

        return cls._storage_types[storage_type](**kwargs)
