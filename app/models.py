from datetime import datetime
from typing import Optional, Dict, Any, Annotated
from pydantic import BaseModel, Field, BeforeValidator
from bson import ObjectId

def validate_object_id(v: Any) -> ObjectId:
    if isinstance(v, ObjectId):
        return v
    if isinstance(v, str):
        return ObjectId(v)
    raise ValueError("Invalid ObjectId")

def objectid_json_schema(schema, handler):
    json_schema = handler(schema)
    json_schema.update(type='string', format='objectid')
    return json_schema

PyObjectId = Annotated[
    ObjectId, 
    BeforeValidator(validate_object_id),
    Field(json_schema_extra=objectid_json_schema)
]

class MongoBaseModel(BaseModel):
    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str}
    }
    
    id: Optional[str] = Field(default=None, alias="_id")

class User(MongoBaseModel):
    name: str
    email: str
    age: Optional[int] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class Item(MongoBaseModel):
    name: str
    description: Optional[str] = None
    price: float
    quantity: int = 0
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)