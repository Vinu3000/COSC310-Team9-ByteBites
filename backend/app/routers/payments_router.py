from fastapi import APIRouter, HTTPException

router = APIRouter()

order_service = None


def set_order_service(service):
    global order_service
    order_service = service


@router.post("/payments/{order_id}")
def process_payment(order_id: str, payload: dict):
    try:
        payment_method = payload["payment_method"]
        card_number = payload.get("card_number")
        return order_service.process_order_payment(order_id, payment_method, card_number)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))