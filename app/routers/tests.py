from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import current_user
from app.models import DiagnosticCentre, DiagnosticTest
from app.schemas import TestCreate, TestResponse

router = APIRouter(prefix="/tests", tags=["Diagnostic Tests"])

@router.post("/", response_model=TestResponse, status_code=201)
def create_test(data: TestCreate, db: Session = Depends(get_db), user=Depends(current_user)):
    if not db.get(DiagnosticCentre, data.centre_id):
        raise HTTPException(404, "Diagnostic centre not found")
    test = DiagnosticTest(**data.model_dump())
    db.add(test); db.commit(); db.refresh(test)
    return test

@router.get("/", response_model=list[TestResponse])
def list_tests(db: Session = Depends(get_db)):
    return db.query(DiagnosticTest).all()
