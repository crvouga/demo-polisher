import os
import shutil
from typing import BinaryIO, Optional, Union
from src.object_storage.inter import ObjectStorage


class LocalObjectStorage(ObjectStorage):
    """
    Local filesystem implementation of ObjectStorage interface.
    Stores objects as files in a specified base directory.
    """

    def __init__(self, base_dir: str):
        """
        Initialize local storage with a base directory.

        Args:
            base_dir (str): Base directory where objects will be stored
        """
        self.base_dir = base_dir
        os.makedirs(base_dir, exist_ok=True)

    def _get_full_path(self, object_name: str) -> str:
        """Get the full filesystem path for an object."""
        return os.path.join(self.base_dir, object_name)

    def upload(
        self,
        object_name: str,
        data: Union[bytes, BinaryIO, str],
        content_type: Optional[str] = None,
        metadata: Optional[dict] = None,
    ) -> str:
        """
        Upload an object to local storage.

        Args:
            object_name (str): Name/path for the object in storage
            data (Union[bytes, BinaryIO, str]): The data to upload, can be bytes, file-like object, or path to file
            content_type (Optional[str]): MIME type of the object (ignored in local implementation)
            metadata (Optional[dict]): Additional metadata for the object (ignored in local implementation)

        Returns:
            str: Path to the uploaded file
        """
        full_path = self._get_full_path(object_name)

        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        if isinstance(data, bytes):
            with open(full_path, "wb") as f:
                f.write(data)
        elif isinstance(data, str) and os.path.isfile(data):
            shutil.copy2(data, full_path)
        elif hasattr(data, "read"):
            with open(full_path, "wb") as f:
                shutil.copyfileobj(data, f)
        else:
            raise ValueError("Data must be bytes, file path, or file-like object")

        return full_path

    def download(
        self, object_name: str, destination: Optional[Union[str, BinaryIO]] = None
    ) -> Union[bytes, str]:
        """
        Download an object from local storage.

        Args:
            object_name (str): Name/path of the object to download
            destination (Optional[Union[str, BinaryIO]]): Path or file-like object to save to.
                                                         If None, returns the data as bytes.

        Returns:
            Union[bytes, str]: Object data as bytes if no destination provided,
                              or path where the file was saved
        """
        full_path = self._get_full_path(object_name)

        if not os.path.exists(full_path):
            raise FileNotFoundError(f"Object {object_name} does not exist")

        if destination is None:
            with open(full_path, "rb") as f:
                return f.read()
        elif isinstance(destination, str):
            os.makedirs(os.path.dirname(destination), exist_ok=True)
            shutil.copy2(full_path, destination)
            return destination
        else:
            with open(full_path, "rb") as f:
                shutil.copyfileobj(f, destination)
            return destination

    def delete(self, object_name: str) -> bool:
        """
        Delete an object from local storage.

        Args:
            object_name (str): Name/path of the object to delete

        Returns:
            bool: True if deletion was successful, False otherwise
        """
        full_path = self._get_full_path(object_name)

        if not os.path.exists(full_path):
            return False

        try:
            os.remove(full_path)
            return True
        except Exception:
            return False

    def exists(self, object_name: str) -> bool:
        """
        Check if an object exists in local storage.

        Args:
            object_name (str): Name/path of the object to check

        Returns:
            bool: True if the object exists, False otherwise
        """
        return os.path.exists(self._get_full_path(object_name))

    def get_url(self, object_name: str, expires: Optional[int] = None) -> str:
        """
        Get a URL for accessing the object.
        For local storage, this returns a file:// URL.

        Args:
            object_name (str): Name/path of the object
            expires (Optional[int]): Expiration time in seconds (ignored in local implementation)

        Returns:
            str: URL for accessing the object
        """
        full_path = self._get_full_path(object_name)
        return f"file://{os.path.abspath(full_path)}"
