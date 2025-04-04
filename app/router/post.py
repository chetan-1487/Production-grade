from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import model
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List
from ..metadata import DownloadRequest
from ..download import download_video
import os

router=APIRouter(
    tags=['User Information']
)


# @router.get("/metadata")
# async def get_metadata(url:str,db:Session=Depends(get_db)):
#     info=ydl.extract_info(url,download=False)
#     return {
#         "title":info.get("title"),
#         "duration":info.get("duration"),
#         "views":info.get("view_count"),
#         "likes":info.get("like_count"),
#         "channel":info.get("uploader"),
#         "thumbnail_url":info.get("thumbnail"),
#         "published_date":info.get("upload_date")
#     }


@router.post("/download")
async def download(request:DownloadRequest):
    filepath, metadata_dict=download_video(request.url,request.quality,request.format)
    if not filepath:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Download failed")
    with get_session() as session:
        metadata = Video_Metadata(**metadata_dict)
        session.add(metadata)
        session.commit()

    # return {
    #     "download_path": filepath,
    #     "metadata": metadata_dict
    # }
    return {"status":"Success","Message":"Download Started"}