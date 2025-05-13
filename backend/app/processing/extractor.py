from typing import Dict, Any
import logging
from app.processing.ocr import process_document
from app.utils.file_handling import save_temp_file, cleanup_temp_file
from datetime import datetime

logger = logging.getLogger(__name__)

async def extract_document_data(file_data: bytes, file_type: str) -> Dict[str, Any]:
    """Process document and extract data"""
    try:
        # Save to temp file for processing
        temp_file_path = save_temp_file(file_data, file_type)
        
        # Process the document
        full_text, key_value_pairs = process_document(file_data, file_type)
        
        # Cleanup
        cleanup_temp_file(temp_file_path)
        
        return {
            "full_text": full_text,
            "key_value_pairs": key_value_pairs,
            "metadata": {
                "processing_time": datetime.now().isoformat(),
                "pages_processed": len(full_text.split('--- PAGE')) - 1 if '--- PAGE' in full_text else 1
            }
        }
    except Exception as e:
        logger.error(f"Error in document extraction: {e}")
        raise