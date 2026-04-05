from fastapi import HTTPException
from typing import Dict, Any


class RefundService:
    ALLOWED_ORDER_STATUSES = {"Pending", "Preparing"}
    SUCCESS_PAYMENT_STATUS = "Success"

    def request_refund(self, order: Dict[str, Any], reason: str | None = None) -> Dict[str, Any]:
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")

        if order.get("payment_status") != self.SUCCESS_PAYMENT_STATUS:
            raise HTTPException(status_code=400, detail="Refund allowed only for successfully paid orders")

        if order.get("status") not in self.ALLOWED_ORDER_STATUSES:
            raise HTTPException(
                status_code=400,
                detail="Refund allowed only for orders in Pending or Preparing status",
            )

        if order.get("refund_status") in {"Requested", "Approved"}:
            raise HTTPException(status_code=400, detail="Refund already requested for this order")

        order["refund_status"] = "Requested"
        order["refund_reason"] = reason

        return {
            "order_id": order["id"],
            "refund_status": order["refund_status"],
            "message": "Refund request submitted successfully",
        }

    def approve_refund(self, order: Dict[str, Any]) -> Dict[str, Any]:
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")

        if order.get("refund_status") != "Requested":
            raise HTTPException(status_code=400, detail="No pending refund request for this order")

        order["refund_status"] = "Approved"
        order["payment_status"] = "Refunded"
        order["status"] = "Cancelled"

        return {
            "order_id": order["id"],
            "refund_status": order["refund_status"],
            "message": "Refund approved successfully",
        }

    def reject_refund(self, order: Dict[str, Any]) -> Dict[str, Any]:
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")

        if order.get("refund_status") != "Requested":
            raise HTTPException(status_code=400, detail="No pending refund request for this order")

        order["refund_status"] = "Rejected"

        return {
            "order_id": order["id"],
            "refund_status": order["refund_status"],
            "message": "Refund rejected successfully",
        }
