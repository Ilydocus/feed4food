from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import ProduceReport
from pydantic import BaseModel
from datetime import date

router = APIRouter()

class ReportCreate(BaseModel):
    user_id: int
    date: date
    produce_type: str
    quantity: float
    remarks: str = None

@router.post("/reports")
def create_report(report: ReportCreate, db: Session = Depends(get_db)):
    new_report = ProduceReport(**report.dict())
    db.add(new_report)
    db.commit()
    db.refresh(new_report)
    return new_report
