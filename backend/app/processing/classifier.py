import logging
from typing import Dict, Optional
import magic
import re

logger = logging.getLogger(__name__)

class DocumentClassifier:
    """Classify documents and extract metadata"""
    
    @staticmethod
    def classify_document(file_data: bytes, filename: str) -> Dict:
        """Classify document type and extract basic metadata"""
        try:
            mime = magic.Magic(mime=True)
            file_type = mime.from_buffer(file_data)
            
            metadata = {
                "type": file_type,
                "size": len(file_data),
                "filename": filename,
                "is_text": False,
                "is_image": False,
                "is_pdf": False,
                "is_office_doc": False
            }
            
            if file_type.startswith("text/"):
                metadata["is_text"] = True
                metadata["encoding"] = "utf-8"
            elif file_type.startswith("image/"):
                metadata["is_image"] = True
            elif file_type == "application/pdf":
                metadata["is_pdf"] = True
            elif "word" in file_type or "excel" in file_type or "powerpoint" in file_type:
                metadata["is_office_doc"] = True
            
            # Try to extract additional metadata from filename
            metadata.update(DocumentClassifier._extract_filename_metadata(filename))
            
            return metadata
        except Exception as e:
            logger.error(f"Error classifying document: {e}")
            raise
    
    @staticmethod
    def _extract_filename_metadata(filename: str) -> Dict:
        """Extract metadata from filename patterns"""
        metadata = {}
        
        # Common patterns
        date_patterns = [
            r'\d{4}-\d{2}-\d{2}',  # YYYY-MM-DD
            r'\d{2}-\d{2}-\d{4}',  # DD-MM-YYYY
            r'\d{8}',              # YYYYMMDD
        ]
        
        for pattern in date_patterns:
            match = re.search(pattern, filename)
            if match:
                metadata["filename_date"] = match.group()
                break
        
        # Invoice numbers, IDs, etc.
        id_pattern = r'[A-Z]{2,3}-\d{4,6}'
        match = re.search(id_pattern, filename)
        if match:
            metadata["filename_id"] = match.group()
        
        return metadata