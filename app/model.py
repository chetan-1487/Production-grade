from sqlalchemy import Column,Integer,String
from database import Base

class post(Base):
    __tablename__="Download_history"
    title=Column(String,nullable=False)
    duration=Column(String,nullable=False)
    views=Column(Integer,nullable=False)
    likes=Column(Integer,nullable=False)
    channel=Column(String,nullable=False)
    thumbnail_url=Column(String,nullable=False)
    published_date=Column(String,nullable=False)