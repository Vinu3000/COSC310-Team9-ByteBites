from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import auth, items, orders, restaurants, notifications, payments, promo
from app.database import engine, Base
from app.repositories.order_repository import OrderRepository
from app.repositories.notification_repository import NotificationRepository
from app.services.pricing_service import PricingService
from app.services.payment_service import PaymentService
from app.services.notification_service import NotificationService
from app.services.order_service import OrderService
from app.routers.refunds_router import router as refunds_router

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(redirect_slashes=False)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Services
pricing_service = PricingService()
payment_service = PaymentService()
order_repo = OrderRepository()
notif_repo = NotificationRepository()
notif_service = NotificationService(notif_repo)
order_service = OrderService(order_repo, pricing_service, payment_service, notif_service)

# API routes used by frontend
app.include_router(auth.router, prefix="/api/v1/auth")
app.include_router(items.router, prefix="/api/v1/menu")
app.include_router(restaurants.router, prefix="/api/v1/restaurants")
app.include_router(orders.router, prefix="/api/v1/orders")
app.include_router(payments.router, prefix="/api/v1/payments")
app.include_router(notifications.router, prefix="/api/v1/notifications")
app.include_router(promo.router, prefix="/api/v1/promos", tags=["promos"])
app.include_router(refunds_router, prefix="/api/v1")

# Extra refund routes used by backend tests
app.include_router(refunds_router)


app.include_router(refunds_router, prefix="/api/v1")  # frontend
app.include_router(refunds_router)                   # tests

@app.get("/")
def home():
    return {"message": "ByteBites API is running!"}