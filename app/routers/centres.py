from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import current_user
from app.models import DiagnosticCentre
from app.schemas import CentreCreate, CentreResponse

router = APIRouter(prefix="/centres", tags=["Diagnostic Centres"])

@router.post("/", response_model=CentreResponse, status_code=201)
def create_centre(data: CentreCreate, db: Session = Depends(get_db), user=Depends(current_user)):
    centre = DiagnosticCentre(**data.model_dump())
    db.add(centre); db.commit(); db.refresh(centre)
    return centre

@router.get("/", response_model=list[CentreResponse])
def list_centres(db: Session = Depends(get_db)):
    return db.query(DiagnosticCentre).all()
