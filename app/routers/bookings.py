from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import current_user
from app.models import Booking, DiagnosticCentre, DiagnosticTest
from app.schemas import BookingCreate, BookingResponse

router = APIRouter(prefix="/bookings", tags=["Bookings"])

@router.post("/", response_model=BookingResponse, status_code=201)
def create_booking(data: BookingCreate, db: Session = Depends(get_db), user=Depends(current_user)):
    test = db.get(DiagnosticTest, data.test_id)
    centre = db.get(DiagnosticCentre, data.centre_id)
    if not test or not centre:
        raise HTTPException(404, "Test or centre not found")
    if test.centre_id != centre.id:
        raise HTTPException(400, "Test is not offered by this centre")
    booking = Booking(
        user_id=user.id,
        test_id=test.id,
        centre_id=centre.id,
        appointment_at=data.appointment_at,
        amount=test.price,
        status="PENDING",
    )
    db.add(booking); db.commit(); db.refresh(booking)
    return booking

@router.get("/", response_model=list[BookingResponse])
def my_bookings(db: Session = Depends(get_db), user=Depends(current_user)):
    return db.query(Booking).filter(Booking.user_id == user.id).all()

@router.get("/{booking_id}", response_model=BookingResponse)
def get_booking(booking_id: int, db: Session = Depends(get_db), user=Depends(current_user)):
    booking = db.get(Booking, booking_id)
    if not booking:
        raise HTTPException(404, "Booking not found")
    if booking.user_id != user.id:
        raise HTTPException(403, "Not authorized")
    return booking
