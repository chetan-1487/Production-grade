from pydantic import BaseModel
from datetime import datetime


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