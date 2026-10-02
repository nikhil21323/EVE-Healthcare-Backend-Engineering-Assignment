from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, ConfigDict, EmailStr, Field

class SignupRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class CentreCreate(BaseModel):
    name: str
    location: str

class CentreResponse(CentreCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)

class TestCreate(BaseModel):
    name: str
    price: Decimal = Field(gt=0)
    centre_id: int

class TestResponse(TestCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)

class BookingCreate(BaseModel):
    test_id: int
    centre_id: int
    appointment_at: datetime

class BookingResponse(BaseModel):
    id: int
    user_id: int
    test_id: int
    centre_id: int
    appointment_at: datetime
    amount: Decimal
    status: str
    model_config = ConfigDict(from_attributes=True)

class PaymentRequest(BaseModel):
    booking_id: int

class WebhookRequest(BaseModel):
    event_id: str
    booking_id: int
    status: str
