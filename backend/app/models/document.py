from datetime import datetime
from typing import List, Dict, Optional
from pydantic import BaseModel
from enum import Enum

class DocumentStatus(str, Enum):
    UPLOADED = "UPLOADED"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class DocumentBase(BaseModel):
    filename: str
    content_type: str
    size: int
    upload_date: datetime

class DocumentCreate(DocumentBase):
    pass

class Document(DocumentBase):
    id: str
    owner_id: str
    status: DocumentStatus
    extracted_data: Optional[Dict] = None
    processed_pages: int = 0
    total_pages: int = 0
    
    class Config:
        from_attributes = True

class DocumentUpdate(BaseModel):
    status: Optional[DocumentStatus] = None
    extracted_data: Optional[Dict] = None
    processed_pages: Optional[int] = None