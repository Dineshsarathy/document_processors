import pytesseract
from PIL import Image
import pdf2image
import io
import os
import tempfile
from typing import Dict, List, Tuple
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def extract_text_from_image(image_data: bytes) -> str:
    """Extract text from image bytes using Tesseract OCR"""
    try:
        image = Image.open(io.BytesIO(image_data))
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        logger.error(f"Error extracting text from image: {e}")
        raise

def convert_pdf_to_images(pdf_data: bytes, dpi: int = 300) -> List[bytes]:
    """Convert PDF to a list of image bytes"""
    try:
        images = pdf2image.convert_from_bytes(pdf_data, dpi=dpi)
        image_bytes_list = []
        for image in images:
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='JPEG')
            image_bytes_list.append(img_byte_arr.getvalue())
        return image_bytes_list
    except Exception as e:
        logger.error(f"Error converting PDF to images: {e}")
        raise

def process_document(file_data: bytes, file_type: str) -> Tuple[str, Dict]:
    """Process document and extract text and key-value pairs"""
    try:
        full_text = ""
        key_value_pairs = {}
        
        if file_type in ['image/jpeg', 'image/png']:
            full_text = extract_text_from_image(file_data)
            key_value_pairs = extract_key_value_pairs(full_text)
        elif file_type == 'application/pdf':
            images = convert_pdf_to_images(file_data)
            for i, image_data in enumerate(images):
                page_text = extract_text_from_image(image_data)
                full_text += f"\n--- PAGE {i+1} ---\n{page_text}\n"
                if i == 0:  # Extract key-value pairs from first page only
                    key_value_pairs = extract_key_value_pairs(page_text)
        elif file_type in ['text/plain', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']:
            # For text and Word docs, we can read directly
            full_text = file_data.decode('utf-8')
            key_value_pairs = extract_key_value_pairs(full_text)
        else:
            raise ValueError(f"Unsupported file type: {file_type}")
        
        return full_text, key_value_pairs
    except Exception as e:
        logger.error(f"Error processing document: {e}")
        raise

def extract_key_value_pairs(text: str) -> Dict:
    """Extract key-value pairs from text using simple pattern matching"""
    # This is a simple implementation - you might want to use more sophisticated NLP techniques
    # or template matching for specific document types
    pairs = {}
    
    # Common patterns
    patterns = [
        (r'([A-Z][a-zA-Z\s]+):\s*(.+)', 'colon separated'),
        (r'([A-Z][a-zA-Z\s]+)\s*=\s*(.+)', 'equals separated'),
        (r'(?<=\n)([A-Z][a-zA-Z\s]+)\s+([^\n]+)', 'line separated'),
    ]
    
    import re
    for pattern, _ in patterns:
        matches = re.findall(pattern, text)
        for match in matches:
            key = match[0].strip()
            value = match[1].strip()
            if key and value:
                pairs[key] = value
    
    # Try to extract dates, amounts, etc.
    date_matches = re.findall(r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})', text)
    if date_matches:
        pairs['extracted_dates'] = date_matches
        
    amount_matches = re.findall(r'(\$\d+\.\d{2})', text)
    if amount_matches:
        pairs['extracted_amounts'] = amount_matches
    
    return pairs