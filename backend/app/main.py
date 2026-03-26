from fastapi import FastAPI
from app.api.v1 import auth, items, orders, restaurants, notifications, payments
from app.database import engine, Base
from app.repositories.order_repository import OrderRepository
from app.repositories.notification_repository import NotificationRepository
from app.services.pricing_service import PricingService
from app.services.payment_service import PaymentService
from app.services.notification_service import NotificationService
from app.services.order_service import OrderService

Base.metadata.create_all(bind=engine)
app = FastAPI()

# Setup all services
pricing_service = PricingService()
payment_service = PaymentService()
order_repo = OrderRepository()
notif_repo = NotificationRepository()
notif_service = NotificationService(notif_repo)
order_service = OrderService(order_repo, pricing_service, payment_service, notif_service)

# Register all routes under /api/v1
app.include_router(auth.router, prefix="/api/v1/auth")
app.include_router(items.router, prefix="/api/v1/menu")
app.include_router(restaurants.router, prefix="/api/v1/restaurants")
app.include_router(orders.router, prefix="/api/v1/orders")
app.include_router(payments.router, prefix="/api/v1/payments")
app.include_router(notifications.router, prefix="/api/v1/notifications")

@app.get("/")
def home():
    return {"message": "ByteBites API is running!"}