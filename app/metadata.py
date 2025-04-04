from pydantic import BaseModel
from datetime import datetime


class DownloadRequest(BaseModel):
    url:str
    format:str
    quality:str
