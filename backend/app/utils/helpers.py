from datetime import datetime
from typing import Any, Dict
import json
from bson import ObjectId
from fastapi.encoders import jsonable_encoder

class JSONEncoder(json.JSONEncoder):
    """Custom JSON encoder that handles MongoDB ObjectId and datetime"""
    def default(self, o: Any) -> Any:
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime):
            return o.isoformat()
        return super().default(o)

def serialize_dict(d: Dict) -> Dict:
    """Serialize a dictionary containing MongoDB-specific types"""
    return json.loads(JSONEncoder().encode(d))

def prepare_response(data: Any) -> Any:
    """Prepare data for API response"""
    if isinstance(data, list):
        return [serialize_dict(item) for item in data]
    if isinstance(data, dict):
        return serialize_dict(data)
    return jsonable_encoder(data)

def validate_object_id(id: str) -> ObjectId:
    """Validate and convert string to MongoDB ObjectId"""
    try:
        return ObjectId(id)
    except Exception:
        raise ValueError(f"Invalid ObjectId: {id}")

def get_current_timestamp() -> datetime:
    """Get current UTC timestamp"""
    return datetime.utcnow()