from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from datetime import datetime
from typing import List
from app.models.document import Document, DocumentCreate, DocumentStatus, DocumentUpdate
from app.core.security import get_current_user
from app.core.database import get_database
from app.processing.extractor import extract_document_data
from app.utils.file_handling import save_document_file
from bson import ObjectId
import logging

router = APIRouter()

@router.post("/documents/upload", response_model=Document)
async def upload_document(
    file: UploadFile = File(...),
    current_user: str = Depends(get_current_user)
):
    db = get_database()
    
    try:
        # Read file content
        file_data = await file.read()
        
        # Create document record
        document_data = DocumentCreate(
            filename=file.filename,
            content_type=file.content_type,
            size=len(file_data),
            upload_date=datetime.now()
        )
        
        # Save to database
        document_dict = document_data.dict()
        document_dict["owner_id"] = current_user
        document_dict["status"] = DocumentStatus.UPLOADED.value
        
        result = await db["documents"].insert_one(document_dict)
        document_id = str(result.inserted_id)
        
        # Save file to storage
        await save_document_file(document_id, file_data)
        
        # Start processing in background (in a real app, use Celery or similar)
        await process_document_in_background(document_id, file_data, file.content_type)
        
        # Return the created document
        created_document = await db["documents"].find_one({"_id": result.inserted_id})
        created_document["id"] = document_id
        return created_document
        
    except Exception as e:
        logging.error(f"Error uploading document: {e}")
        raise HTTPException(status_code=500, detail="Error uploading document")

async def process_document_in_background(document_id: str, file_data: bytes, content_type: str):
    db = get_database()
    try:
        # Update status to processing
        await db["documents"].update_one(
            {"_id": ObjectId(document_id)},
            {"$set": {"status": DocumentStatus.PROCESSING.value}}
        )
        
        # Process the document
        extracted_data = await extract_document_data(file_data, content_type)
        
        # Update document with results
        await db["documents"].update_one(
            {"_id": ObjectId(document_id)},
            {"$set": {
                "status": DocumentStatus.COMPLETED.value,
                "extracted_data": extracted_data,
                "processed_pages": extracted_data["metadata"]["pages_processed"],
                "total_pages": extracted_data["metadata"]["pages_processed"]
            }}
        )
        
    except Exception as e:
        logging.error(f"Error processing document {document_id}: {e}")
        await db["documents"].update_one(
            {"_id": ObjectId(document_id)},
            {"$set": {"status": DocumentStatus.FAILED.value}}
        )

@router.get("/", response_model=List[Document])
async def get_user_documents(
    skip: int = 0,
    limit: int = 100,
    current_user: str = Depends(get_current_user)
):
    db = get_database()
    documents = []
    async for doc in db["documents"].find({"owner_id": current_user}).skip(skip).limit(limit):
        doc["id"] = str(doc["_id"])
        documents.append(doc)
    return documents

# @router.get("/{document_id}", response_model=Document)
# async def get_document(
#     document_id: str,
#     current_user: str = Depends(get_current_user)
# ):
#     db = get_database()
#     document = await db["documents"].find_one({"_id": ObjectId(document_id), "owner_id": current_user})
#     if not document:
#         raise HTTPException(status_code=404, detail="Document not found")
#     document["id"] = str(document["_id"])
#     return document

@router.get("/{document_id}", response_model=Document)
async def get_document(
    document_id: str,
    current_user: str = Depends(get_current_user)
):
    db = get_database()
    document = await db["documents"].find_one({"_id": ObjectId(document_id), "owner_id": current_user})
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    document["id"] = str(document["_id"])

    # Extract key-value pairs (can be used to display in a table or other format)
    extracted_data = document.get("extracted_data", {})
    key_value_pairs = extracted_data.get("key_value_pairs", {})

    return {
        "document": document,
        "extracted_data": key_value_pairs  # Include extracted data here
    }