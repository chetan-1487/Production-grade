from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter,Query

from ..Database.models import model
from ..Core import auth2
from sqlalchemy.orm import Session
from ..Database.database import get_db
from typing import List
from ..Schema.metadata import DownloadRequest
from ..Core.Service.download import download_video
import os
from app.Database.models.model import VideoMetadata,DownloadHistory
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, HttpUrl
from ..Schema.metadata import VideoMetadataResponse

router=APIRouter(
    tags=['User Information']
)

# @router.get("/history")
# def get_download_history(db: Session = Depends(get_db),current_user:int=Depends(auth2.get_current_user)):
   


# @router.get("/metadata", response_model=VideoMetadataResponse)
# def get_video_metadata(url: str = Query(..., description="YouTube video URL"), db: Session = Depends(get_db),current_user:int=Depends(auth2.get_current_user)):
#     metadata = db.query(VideoMetadata).filter(VideoMetadata.url == url).first()

#     if not metadata:
#         raise HTTPException(status_code=404, detail="Video metadata not found")

#     return {
#         "title": metadata.title,
#         "duration": metadata.duration,
#         "views": metadata.views,
#         "likes": metadata.likes,
#         "channel": metadata.channel,
#         "thumbnail_url": metadata.thumbnail_url,
#         "published_date": metadata.published_date
#     }

@router.post("/download")
async def download(request: DownloadRequest, db: Session = Depends(get_db),current_user:int=Depends(auth2.get_current_user)):
    filepath, metadata_dict = download_video(request.url, request.quality, request.format)

    if not filepath:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Download failed")

    # Store metadata in DB
    metadata = VideoMetadata(**metadata_dict)
    db.add(metadata)
    db.commit()
    db.refresh(metadata)

    #Store metadata in DownloadHistory
    # history = DownloadHistory(
    #     video_id=metadata.id,
    #     status="Success",
    #     download_date=datetime.utcnow()
    # )
    # db.add(history)
    # db.commit()

    return{
        "Status":"Success",
        "filepath": filepath,
        "title": metadata.title,
        "duration": metadata.duration,
        "views": metadata.views,
        "likes": metadata.likes,
        "channel": metadata.channel,
        "thumbnail_url": metadata.thumbnail_url,
        "published_date": metadata.published_date
    }