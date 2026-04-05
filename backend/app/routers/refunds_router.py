from fastapi import APIRouter
from app.schemas.refund_schema import RefundRequestBody
from app.services.refund_service import RefundService

router = APIRouter(prefix="/refunds", tags=["Refunds"])
refund_service = RefundService()

orders_db = [
    {
        "id": 1,
        "status": "Pending",
        "payment_status": "Success",
        "refund_status": "None",
        "refund_reason": None,
    },
    {
        "id": 2,
        "status": "Completed",
        "payment_status": "Success",
        "refund_status": "None",
        "refund_reason": None,
    },
]


def get_order_by_id(order_id: int):
    for order in orders_db:
        if order["id"] == order_id:
            return order
    return None


@router.post("/{order_id}/request")
def request_refund(order_id: int, body: RefundRequestBody):
    order = get_order_by_id(order_id)
    return refund_service.request_refund(order, body.reason)


@router.put("/{order_id}/approve")
def approve_refund(order_id: int):
    order = get_order_by_id(order_id)
    return refund_service.approve_refund(order)


@router.put("/{order_id}/reject")
def reject_refund(order_id: int):
    order = get_order_by_id(order_id)
    return refund_service.reject_refund(order)
