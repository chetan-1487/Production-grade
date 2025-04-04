from sqlalchemy import Column,Integer,String, ForeignKey, DateTime
from .database import Base
from datetime import datetime

class VideoMetadata(Base):
    __tablename__="Video_Metadata"
    id=Column(Integer,primary_key=True,nullable=False)
    title=Column(String,nullable=False)
    duration=Column(String,nullable=False)
    views=Column(Integer,nullable=False)
    likes=Column(Integer,nullable=False)
    channel=Column(String,nullable=False)
    thumbnail_url=Column(String,nullable=False)
    published_date=Column(String,nullable=False)
    created_at=Column(DateTime,default=datetime.now())
    user_id=Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False)

class User(Base):
    __tablename__="users"
    id=Column(Integer,primary_key=True,nullable=False)
    email=Column(String,nullable=False,unique=True)
    password=Column(String,nullable=False)

class DownloadHistory(Base):
    __tablename__="download_history"
    id=Column(Integer,primary_key=True,nullable=False)
    status=Column(String,nullable=False)
    video_id=Column(Integer,ForeignKey("Video_Metadata.id",ondelete="CASCADE"),nullable=False)
    download_date=Column(DateTime,default=datetime.now())
