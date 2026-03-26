from fastapi import FastAPI

from app.database import engine, Base
from app.api.v1 import auth, items, orders, restaurants
from app.api.v1.notifications import router as api_notifications_router

from app.repositories.order_repository import OrderRepository
from app.repositories.notification_repository import NotificationRepository

from app.services.pricing_service import PricingService
from app.services.payment_service import PaymentService
from app.services.notification_service import NotificationService
from app.services.order_service import OrderService

from app.routers import orders_router, payments_router, notifications_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

order_repository = OrderRepository()
notification_repository = NotificationRepository()

pricing_service = PricingService()
payment_service = PaymentService()
notification_service = NotificationService(notification_repository)

order_service = OrderService(
    order_repository,
    pricing_service,
    payment_service,
    notification_service
)

orders_router.set_order_service(order_service)
payments_router.set_order_service(order_service)
notifications_router.set_notification_service(notification_service)

# Existing API v1 routes
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(items.router, prefix="/api/v1/menu", tags=["Menu"])
app.include_router(restaurants.router, prefix="/api/v1/restaurants", tags=["Restaurants"])
app.include_router(orders.router, prefix="/api/v1/orders", tags=["Orders"])
app.include_router(api_notifications_router, prefix="/api/v1/notifications", tags=["Notifications"])

# Your feature routes
app.include_router(orders_router.router)
app.include_router(payments_router.router)
app.include_router(notifications_router.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to ByteBites API", "version": "v1.0"}