from fastapi import FastAPI

from app.repositories.order_repository import OrderRepository
from app.repositories.notification_repository import NotificationRepository

from app.services.pricing_service import PricingService
from app.services.payment_service import PaymentService
from app.services.notification_service import NotificationService
from app.services.order_service import OrderService

from app.routers import orders_router, payments_router, notifications_router

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

app.include_router(orders_router.router)
app.include_router(payments_router.router)
app.include_router(notifications_router.router)