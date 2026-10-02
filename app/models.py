from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Numeric, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)

class DiagnosticCentre(Base):
    __tablename__ = "diagnostic_centres"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    location = Column(String(255), nullable=False)
    tests = relationship("DiagnosticTest", back_populates="centre", cascade="all, delete-orphan")

class DiagnosticTest(Base):
    __tablename__ = "diagnostic_tests"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    centre_id = Column(Integer, ForeignKey("diagnostic_centres.id", ondelete="CASCADE"), nullable=False)
    centre = relationship("DiagnosticCentre", back_populates="tests")

class Booking(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    test_id = Column(Integer, ForeignKey("diagnostic_tests.id"), nullable=False)
    centre_id = Column(Integer, ForeignKey("diagnostic_centres.id"), nullable=False)
    appointment_at = Column(DateTime, nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    status = Column(String(20), nullable=False, default="PENDING")

class Payment(Base):
    __tablename__ = "payments"
    id = Column(Integer, primary_key=True)
    booking_id = Column(Integer, ForeignKey("bookings.id"), nullable=False)
    provider_event_id = Column(String(255), unique=True, nullable=True, index=True)
    amount = Column(Numeric(10, 2), nullable=False)
    status = Column(String(20), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
