class OrderService:
    VALID_TRANSITIONS = {
        "Pending": ["Preparing"],
        "Preparing": ["OutForDelivery"],
        "OutForDelivery": ["Completed"],
        "Completed": []
    }

    def __init__(self, order_repository, pricing_service, payment_service, notification_service):
        self.order_repository = order_repository
        self.pricing_service = pricing_service
        self.payment_service = payment_service
        self.notification_service = notification_service

    def create_order(self, items, delivery_address):
        pricing = self.pricing_service.calculate_total(items)

        order_data = {
            "items": items,
            "delivery_address": delivery_address,
            "subtotal": pricing["subtotal"],
            "delivery_fee": pricing["delivery_fee"],
            "taxes": pricing["taxes"],
            "total": pricing["total"],
            "status": "Pending",
            "payment_status": None
        }

        return self.order_repository.create(order_data)

    def get_order(self, order_id):
        return self.order_repository.get_by_id(order_id)

    def update_order_status(self, order_id, new_status):
        order = self.order_repository.get_by_id(order_id)

        if not order:
            raise ValueError("Order not found")

        if order["status"] == "Completed":
            raise ValueError("Completed order cannot be modified")

        allowed_statuses = self.VALID_TRANSITIONS[order["status"]]
        if new_status not in allowed_statuses:
            raise ValueError("Invalid status transition")

        order["status"] = new_status
        updated_order = self.order_repository.update(order_id, order)

        self.notification_service.create_notification(
            order_id,
            f"Order status updated to {new_status}"
        )

        return updated_order

    def process_order_payment(self, order_id, payment_method, card_number=None):
        order = self.order_repository.get_by_id(order_id)

        if not order:
            raise ValueError("Order not found")

        if order["status"] == "Completed":
            raise ValueError("Completed order cannot be modified")

        result = self.payment_service.process_payment(payment_method, card_number)
        order["payment_status"] = result

        updated_order = self.order_repository.update(order_id, order)
        return updated_order