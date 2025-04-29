from abc import ABC, abstractmethod
from typing import BinaryIO, Optional, Union


class ObjectStorage(ABC):
    """
    Interface for object storage operations.
    Provides methods for uploading, downloading, and managing objects in storage.
    """

    @abstractmethod
    def upload(
        self,
        object_name: str,
        data: Union[bytes, BinaryIO, str],
        content_type: Optional[str] = None,
        metadata: Optional[dict] = None,
    ) -> str:
        """
        Upload an object to storage.

        Args:
            object_name (str): Name/path for the object in storage
            data (Union[bytes, BinaryIO, str]): The data to upload, can be bytes, file-like object, or path to file
            content_type (Optional[str]): MIME type of the object
            metadata (Optional[dict]): Additional metadata for the object

        Returns:
            str: URL or identifier for the uploaded object
        """
        pass

    @abstractmethod
    def download(
        self, object_name: str, destination: Optional[Union[str, BinaryIO]] = None
    ) -> Union[bytes, str]:
        """
        Download an object from storage.

        Args:
            object_name (str): Name/path of the object to download
            destination (Optional[Union[str, BinaryIO]]): Path or file-like object to save to.
                                                         If None, returns the data as bytes.

        Returns:
            Union[bytes, str]: Object data as bytes if no destination provided,
                              or path where the file was saved
        """
        pass

    @abstractmethod
    def delete(self, object_name: str) -> bool:
        """
        Delete an object from storage.

        Args:
            object_name (str): Name/path of the object to delete

        Returns:
            bool: True if deletion was successful, False otherwise
        """
        pass

    @abstractmethod
    def exists(self, object_name: str) -> bool:
        """
        Check if an object exists in storage.

        Args:
            object_name (str): Name/path of the object to check

        Returns:
            bool: True if the object exists, False otherwise
        """
        pass

    @abstractmethod
    def get_url(self, object_name: str, expires: Optional[int] = None) -> str:
        """
        Get a URL for accessing the object.

        Args:
            object_name (str): Name/path of the object
            expires (Optional[int]): Expiration time in seconds for the URL

        Returns:
            str: URL for accessing the object
        """
        pass
