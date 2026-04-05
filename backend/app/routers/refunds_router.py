from fastapi import APIRouter
from app.schemas.refund_schema import RefundRequestBody
from app.services.refund_service import RefundService

router = APIRouter(prefix="/refunds", tags=["Refunds"])
refund_service = RefundService()


@router.post("/{order_id}/request")
def request_refund(order_id: str, body: RefundRequestBody):
    return refund_service.request_refund(order_id, body.reason)


@router.put("/{order_id}/approve")
def approve_refund(order_id: str):
    return refund_service.approve_refund(order_id)


@router.put("/{order_id}/reject")
def reject_refund(order_id: str):
    return refund_service.reject_refund(order_id)
