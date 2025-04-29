import logging
import os
import shutil
from typing import BinaryIO, Optional, Union
from fastapi import FastAPI, HTTPException, APIRouter
from fastapi.responses import FileResponse
from src.object_storage.inter import ObjectStorage


class LocalObjectStorage(ObjectStorage):
    """
    Local filesystem implementation of ObjectStorage interface.
    Stores objects as files in a specified base directory and serves them via FastAPI.
    """

    def __init__(self, base_dir, base_url, router, logger):
        """
        Initialize local storage with a base directory and FastAPI router.

        Args:
            base_dir (str): Base directory where objects will be stored
            router (APIRouter): FastAPI router to add routes to
        """

        if not isinstance(base_dir, str):
            raise ValueError("Base directory is required")

        if not isinstance(router, APIRouter):
            raise ValueError("FastAPI router is required")

        if not isinstance(logger, logging.Logger):
            raise ValueError("Logger is required")

        if not isinstance(base_url, str):
            raise ValueError("Base URL is required")

        logger = logger.getChild(LocalObjectStorage.__name__)

        self.base_dir = base_dir
        self.base_url = base_url
        self.router = router
        self.logger = logger
        os.makedirs(base_dir, exist_ok=True)
        self.logger.info(
            f"Initialized LocalObjectStorage with base directory: {base_dir}"
        )

        # Add route to serve files - use the correct path that matches the URL pattern
        @router.get("/local-object-storage/{file_path:path}")
        async def serve_file(file_path: str):
            logger.info(f"Serving file: {file_path}")
            full_path = self._get_full_path(file_path)
            logger.info(f"Full path: {full_path}")
            if not os.path.exists(full_path):
                logger.error(f"File not found: {full_path}")
                raise HTTPException(status_code=404, detail="File not found")
            logger.info(f"File found: {full_path}")
            return FileResponse(full_path)

    def _get_full_path(self, object_name: str) -> str:
        """Get the full filesystem path for an object."""
        full_path = os.path.join(self.base_dir, object_name)
        self.logger.debug(f"Generated full path: {full_path} for object: {object_name}")
        return full_path

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
        self.logger.info(f"Uploading object: {object_name}")
        full_path = self._get_full_path(object_name)

        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        self.logger.debug(f"Created directory structure for: {full_path}")

        if isinstance(data, bytes):
            self.logger.debug(f"Uploading bytes data to {full_path}")
            with open(full_path, "wb") as f:
                f.write(data)
        elif isinstance(data, str) and os.path.isfile(data):
            self.logger.debug(f"Copying file from {data} to {full_path}")
            shutil.copy2(data, full_path)
        elif hasattr(data, "read"):
            self.logger.debug(f"Uploading file-like object to {full_path}")
            with open(full_path, "wb") as f:
                shutil.copyfileobj(data, f)
        else:
            self.logger.error(f"Invalid data type for upload: {type(data)}")
            raise ValueError("Data must be bytes, file path, or file-like object")

        self.logger.info(f"Successfully uploaded object: {object_name} to {full_path}")
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
        self.logger.info(f"Downloading object: {object_name}")
        full_path = self._get_full_path(object_name)

        if not os.path.exists(full_path):
            self.logger.error(f"Object not found: {object_name} at {full_path}")
            raise FileNotFoundError(f"Object {object_name} does not exist")

        if destination is None:
            self.logger.debug(f"Reading object content as bytes: {object_name}")
            with open(full_path, "rb") as f:
                content = f.read()
                self.logger.info(
                    f"Successfully read {len(content)} bytes from {object_name}"
                )
                return content
        elif isinstance(destination, str):
            self.logger.debug(f"Copying object to destination path: {destination}")
            os.makedirs(os.path.dirname(destination), exist_ok=True)
            shutil.copy2(full_path, destination)
            self.logger.info(f"Successfully copied {object_name} to {destination}")
            return destination
        else:
            self.logger.debug(f"Copying object to file-like destination")
            with open(full_path, "rb") as f:
                shutil.copyfileobj(f, destination)
            self.logger.info(
                f"Successfully copied {object_name} to file-like destination"
            )
            return destination

    def delete(self, object_name: str) -> bool:
        """
        Delete an object from local storage.

        Args:
            object_name (str): Name/path of the object to delete

        Returns:
            bool: True if deletion was successful, False otherwise
        """
        self.logger.info(f"Deleting object: {object_name}")
        full_path = self._get_full_path(object_name)

        if not os.path.exists(full_path):
            self.logger.warning(f"Cannot delete non-existent object: {object_name}")
            return False

        try:
            os.remove(full_path)
            self.logger.info(f"Successfully deleted object: {object_name}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to delete object {object_name}: {str(e)}")
            return False

    def exists(self, object_name: str) -> bool:
        """
        Check if an object exists in local storage.

        Args:
            object_name (str): Name/path of the object to check

        Returns:
            bool: True if the object exists, False otherwise
        """
        full_path = self._get_full_path(object_name)
        exists = os.path.exists(full_path)
        self.logger.debug(
            f"Checking if object exists: {object_name} - {'Found' if exists else 'Not found'}"
        )
        return exists

    def get_url(self, object_name: str, expires: Optional[int] = None) -> str:
        """
        Get a URL for accessing the object.
        For local storage with FastAPI, this returns an HTTP URL.

        Args:
            object_name (str): Name/path of the object
            expires (Optional[int]): Expiration time in seconds (ignored in local implementation)

        Returns:
            str: URL for accessing the object
        """

        full_path = self._get_full_path(object_name)
        url = f"{self.base_url}{self.router.prefix}/local-object-storage/{full_path}"
        self.logger.debug(f"Generated URL for object {object_name}: {url}")
        return url
