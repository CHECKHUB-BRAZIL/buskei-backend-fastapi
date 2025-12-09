from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db

router = APIRouter()

@router.post("/register")
def register(db: Session = Depends(get_db)):
    # usar db aqui
    pass
