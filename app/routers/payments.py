import random
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import current_user
from app.models import Booking, Payment
from app.schemas import PaymentRequest, WebhookRequest

router = APIRouter(prefix="/payments", tags=["Payments"])

@router.post("/")
def create_payment(data: PaymentRequest, db: Session = Depends(get_db), user=Depends(current_user)):
    booking = db.get(Booking, data.booking_id)
    if not booking:
        raise HTTPException(404, "Booking not found")
    if booking.user_id != user.id:
        raise HTTPException(403, "Not authorized")
    if booking.status not in ("PENDING",):
        raise HTTPException(400, f"Booking cannot be paid in {booking.status} state")

    result = "SUCCESS" if random.choice([True, True, False]) else "FAILED"
    payment = Payment(
        booking_id=booking.id,
        amount=booking.amount,
        status=result,
    )
    booking.status = "CONFIRMED" if result == "SUCCESS" else "FAILED"
    db.add(payment); db.commit(); db.refresh(payment)
    return {"payment_id": payment.id, "status": result, "booking_status": booking.status}

@router.post("/webhook/")
def payment_webhook(data: WebhookRequest, db: Session = Depends(get_db)):
    existing = db.query(Payment).filter(Payment.provider_event_id == data.event_id).first()
    if existing:
        return {"message": "Event already processed", "payment_id": existing.id, "status": existing.status}

    booking = db.get(Booking, data.booking_id)
    if not booking:
        raise HTTPException(404, "Booking not found")
    if data.status not in ("SUCCESS", "FAILED"):
        raise HTTPException(400, "Invalid payment status")

    payment = Payment(
        booking_id=booking.id,
        provider_event_id=data.event_id,
        amount=booking.amount,
        status=data.status,
    )
    booking.status = "CONFIRMED" if data.status == "SUCCESS" else "FAILED"
    db.add(payment); db.commit()
    return {"message": "Webhook processed", "payment_status": data.status, "booking_status": booking.status}
