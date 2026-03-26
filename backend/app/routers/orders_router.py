from fastapi import APIRouter, HTTPException

router = APIRouter()

order_service = None


def set_order_service(service):
    global order_service
    order_service = service


@router.post("/orders", status_code=201)
def create_order(payload: dict):
    try:
        items = payload["items"]
        delivery_address = payload["delivery_address"]
        return order_service.create_order(items, delivery_address)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/orders/{order_id}")
def get_order(order_id: str):
    order = order_service.get_order(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.put("/orders/{order_id}/status")
def update_order_status(order_id: str, payload: dict):
    try:
        new_status = payload["status"]
        return order_service.update_order_status(order_id, new_status)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))