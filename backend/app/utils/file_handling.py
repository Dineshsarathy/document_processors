import os
import tempfile
from pathlib import Path
from typing import Union
import shutil
from fastapi import UploadFile
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

# Ensure temp storage directory exists
temp_storage = Path(settings.temp_storage_path if hasattr(settings, 'temp_storage_path') else "temp_storage")
temp_storage.mkdir(parents=True, exist_ok=True)

def save_temp_file(file_data: Union[bytes, UploadFile], file_type: str = None) -> str:
    """Save file data to a temporary file and return its path"""
    try:
        suffix = ""
        if file_type:
            if file_type == "application/pdf":
                suffix = ".pdf"
            elif file_type.startswith("image/"):
                suffix = ".jpg"  # Default image suffix
            elif file_type == "text/plain":
                suffix = ".txt"
            elif "word" in file_type:
                suffix = ".docx"
        
        # Create a named temporary file
        temp_file = tempfile.NamedTemporaryFile(
            dir=temp_storage,
            suffix=suffix,
            delete=False
        )
        
        if isinstance(file_data, UploadFile):
            # For UploadFile, read in chunks
            file_data.file.seek(0)
            while chunk := file_data.file.read(1024 * 1024):  # 1MB chunks
                temp_file.write(chunk)
        else:
            # For bytes, write directly
            temp_file.write(file_data)
        
        temp_file.close()
        return temp_file.name
    except Exception as e:
        logger.error(f"Error saving temporary file: {e}")
        raise

def cleanup_temp_file(file_path: str):
    """Clean up a temporary file"""
    try:
        if os.path.exists(file_path):
            os.unlink(file_path)
    except Exception as e:
        logger.error(f"Error cleaning up temporary file {file_path}: {e}")

async def save_document_file(document_id: str, file_data: bytes):
    """Save document file to persistent storage"""
    try:
        doc_storage = temp_storage / "documents"
        doc_storage.mkdir(parents=True, exist_ok=True)
        
        file_path = doc_storage / f"{document_id}.dat"
        with open(file_path, "wb") as f:
            f.write(file_data)
    except Exception as e:
        logger.error(f"Error saving document file {document_id}: {e}")
        raise

async def load_document_file(document_id: str) -> bytes:
    """Load document file from persistent storage"""
    try:
        file_path = temp_storage / "documents" / f"{document_id}.dat"
        with open(file_path, "rb") as f:
            return f.read()
    except Exception as e:
        logger.error(f"Error loading document file {document_id}: {e}")
        raise