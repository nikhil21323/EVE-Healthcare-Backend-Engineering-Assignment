from fastapi import FastAPI
from app.routers import auth, centres, tests, bookings, payments

app = FastAPI(title="EVE Healthcare Diagnostic Booking API", version="1.0.0")

app.include_router(auth.router)
app.include_router(centres.router)
app.include_router(tests.router)
app.include_router(bookings.router)
app.include_router(payments.router)

@app.get("/health")
def health():
    return {"status": "ok"}
