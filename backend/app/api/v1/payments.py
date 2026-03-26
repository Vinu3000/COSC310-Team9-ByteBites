from fastapi import APIRouter, HTTPException, Depends
from app.services.payment_service import PaymentService
router = APIRouter(tags=["Payments"])

def get_payment_service():
    from app.main import payment_service
    return payment_service

@router.post("/process")
async def process_payment(order_id: str, payment_method: str, service: PaymentService = Depends(get_payment_service)):
    """
    Feat6-FR1: Process payment for an order.
    Refactored to use the central PaymentService.
    """
    try:
        result = service.process_payment(payment_method)
        return {"order_id": order_id, "status": "Success", "transaction_id": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))