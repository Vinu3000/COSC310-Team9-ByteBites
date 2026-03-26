from app.models.enums import OrderStatus

class OrderService:
    # Use the Enum in the transition map
    VALID_TRANSITIONS = {
        OrderStatus.PENDING: [OrderStatus.PREPARING, OrderStatus.CANCELLED],
        OrderStatus.PREPARING: [OrderStatus.SHIPPING],
        OrderStatus.SHIPPING: [OrderStatus.COMPLETED],
        OrderStatus.COMPLETED: []
    }

    def __init__(self, order_repository, pricing_service, payment_service, notification_service):
        self.order_repository = order_repository
        self.pricing_service = pricing_service
        self.payment_service = payment_service
        self.notification_service = notification_service

    def create_order(self, items, delivery_address):
        """ Calculate total and save a new order with PENDING status """
        pricing = self.pricing_service.calculate_total(items)

        order_data = {
            "items": items,
            "delivery_address": delivery_address,
            "subtotal": pricing["subtotal"],
            "delivery_fee": pricing["delivery_fee"],
            "taxes": pricing["taxes"],
            "total": pricing["total"],
            "status": OrderStatus.PENDING,
            "payment_status": None
        }
        return self.order_repository.create(order_data)

    def _get_order_or_fail(self, order_id):
        """ Helper method to handle 'Not Found' errors in one place (DRY) """
        order = self.order_repository.get_by_id(order_id)
        if not order:
            raise ValueError(f"Order {order_id} not found")
        return order

    def update_order_status(self, order_id, new_status: OrderStatus):
        """ Handle status changes with validation logic """
        order = self._get_order_or_fail(order_id)

        # Guard Clause: Prevent modification of finished orders
        if order["status"] == OrderStatus.COMPLETED:
            raise ValueError("Completed order cannot be modified")

        # Validate transition using our map
        allowed = self.VALID_TRANSITIONS.get(order["status"], [])
        if new_status not in allowed:
            raise ValueError(f"Invalid transition from {order['status']} to {new_status}")

        # Update data and notify user
        order["status"] = new_status
        updated_order = self.order_repository.update(order_id, order)
        
        self.notification_service.create_notification(
            order_id, 
            f"Order status updated to {new_status}"
        )
        return updated_order

    def process_order_payment(self, order_id, payment_method, card_number=None):
        """ Process payment and update order record """
        order = self._get_order_or_fail(order_id)

        if order["status"] == OrderStatus.COMPLETED:
            raise ValueError("Completed order cannot be modified")

        result = self.payment_service.process_payment(payment_method, card_number)
        order["payment_status"] = result

        return self.order_repository.update(order_id, order)