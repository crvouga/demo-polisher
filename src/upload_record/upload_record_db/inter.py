from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import datetime
from src.upload_record.upload_record import UploadRecord


class UploadRecordRepository(ABC):
    """
    Interface for upload record repository operations.
    Provides methods for creating, retrieving, updating, and deleting upload records.
    """

    @abstractmethod
    async def get(self, id: str) -> Optional[UploadRecord]:
        """
        Retrieve an upload record by its ID.

        Args:
            id (str): The ID of the upload record to retrieve

        Returns:
            Optional[UploadRecord]: The upload record if found, None otherwise
        """
        pass

    @abstractmethod
    async def put(self, upload_record: UploadRecord) -> UploadRecord:
        """
        Create or update an upload record.

        Args:
            upload_record (UploadRecord): The upload record to create or update

        Returns:
            UploadRecord: The created or updated upload record
        """
        pass

    @abstractmethod
    async def zap(self, id: str) -> bool:
        """
        Delete an upload record by its ID.

        Args:
            id (str): The ID of the upload record to delete

        Returns:
            bool: True if deletion was successful, False otherwise
        """
        pass
