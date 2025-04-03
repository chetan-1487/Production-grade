from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import model
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List

router=APIRouter(
    tags=['User Information']
)

@router.get("/metadata")
def User_Info(url:str,db:Session=Depends(get_db)):
    return url

@router.get("/history")
def user_history(db:Session=Depends(get_db)):
    return 

@router.post("/download")
def download(db:Session=Depends(get_db)):
    return