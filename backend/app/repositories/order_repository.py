import uuid


class OrderRepository:
    def __init__(self):
        self.orders = {}

    def create(self, order_data):
        order_id = str(uuid.uuid4())
        order_data["id"] = order_id
        self.orders[order_id] = order_data
        return order_data

    def get_by_id(self, order_id):
        return self.orders.get(order_id)

    def update(self, order_id, updated_order):
        self.orders[order_id] = updated_order
        return updated_order

    def get_all(self):
        return list(self.orders.values())