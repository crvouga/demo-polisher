from dataclasses import dataclass
import datetime


@dataclass
class UploadRecord:
    id: str
    name: str
    uploaded_file_url: str
    separated_file_url: str
    created_at: datetime
