from fastapi import HTTPException
from app.models.enums import OrderStatus
from app.api.v1.shared_data import mock_orders_db


class RefundService:
    ALLOWED_ORDER_STATUSES = {OrderStatus.PENDING, OrderStatus.PREPARING}

    def request_refund(self, order_id: str, reason: str | None = None):
        order = mock_orders_db.get(order_id)

        if not order:
            raise HTTPException(status_code=404, detail="Order not found")

        if order.get("payment_status") != "Success":
            raise HTTPException(
                status_code=400,
                detail="Refund allowed only for successfully paid orders",
            )

        if order.get("status") not in self.ALLOWED_ORDER_STATUSES:
            raise HTTPException(
                status_code=400,
                detail="Refund allowed only for orders in Pending or Preparing status",
            )

        if order.get("refund_status") in {"Requested", "Approved"}:
            raise HTTPException(
                status_code=400,
                detail="Refund already requested for this order",
            )

        order["refund_status"] = "Requested"
        order["refund_reason"] = reason

        return {
            "order_id": order["id"],
            "refund_status": order["refund_status"],
            "message": "Refund request submitted successfully",
        }

    def approve_refund(self, order_id: str):
        order = mock_orders_db.get(order_id)

        if not order:
            raise HTTPException(status_code=404, detail="Order not found")

        if order.get("refund_status") != "Requested":
            raise HTTPException(
                status_code=400,
                detail="No pending refund request for this order",
            )

        order["refund_status"] = "Approved"
        order["payment_status"] = "Refunded"
        order["status"] = OrderStatus.CANCELLED

        return {
            "order_id": order["id"],
            "refund_status": order["refund_status"],
            "payment_status": order["payment_status"],
            "order_status": order["status"],
            "message": "Refund approved successfully",
        }

    def reject_refund(self, order_id: str):
        order = mock_orders_db.get(order_id)

        if not order:
            raise HTTPException(status_code=404, detail="Order not found")

        if order.get("refund_status") != "Requested":
            raise HTTPException(
                status_code=400,
                detail="No pending refund request for this order",
            )

        order["refund_status"] = "Rejected"

        return {
            "order_id": order["id"],
            "refund_status": order["refund_status"],
            "payment_status": order.get("payment_status"),
            "order_status": order.get("status"),
            "message": "Refund rejected successfully",
        }