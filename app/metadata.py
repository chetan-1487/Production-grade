from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from typing import Optional
from uuid import UUID as uuid

class UserCreate(BaseModel):
    email:str
    password:str

class Userout(BaseModel):
    id:uuid
    email:str
    created_at:datetime

    model_config = ConfigDict(from_attributes=True)
    
class UserLogin(BaseModel):
    email:EmailStr
    password:str

class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    id:uuid

class DownloadRequest(BaseModel):
    url:str
    format:str
    quality:str

class VideoMetadataResponse(BaseModel):
    title:str
    duration:str
    views:int
    likes:int
    channel:str
    thumbnail_url:str
    published_date:str