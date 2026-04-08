from fastapi import APIRouter, HTTPException, Body
from app.api.v1.shared_data import mock_promos_db

router = APIRouter()

# 1. Admin Function: Get all promos to show on the Admin Page
@router.get("/")
async def get_all_promos():
    return list(mock_promos_db.values())

# 2. Admin Function: Toggle a promo's active status (The "Control" part)
@router.patch("/{promo_id}/toggle")
async def toggle_promo(promo_id: int):
    # Find the promo in our mock database
    for code in mock_promos_db:
        if mock_promos_db[code]["id"] == promo_id:
            # Switch True to False or False to True
            mock_promos_db[code]["is_active"] = not mock_promos_db[code]["is_active"]
            return mock_promos_db[code]
    raise HTTPException(status_code=404, detail="Promo not found")

# 3. User Function: Apply a promo to an order
@router.post("/apply")
async def apply_promo(data: dict = Body(...)):
    # .upper() makes it case-insensitive (e.g., student5 works too)
    code = data.get("code", "").upper()
    subtotal = data.get("subtotal", 0)

    if code not in mock_promos_db:
        raise HTTPException(status_code=404, detail="This code does not exist.")

    promo = mock_promos_db[code]

    # CHECK: Is the promo currently turned off by the Admin?
    if not promo["is_active"]:
        raise HTTPException(status_code=400, detail="This promo has been disabled by the admin.")

    # CHECK: Did the user spend enough?
    if subtotal < promo["min_spend"]:
        raise HTTPException(status_code=400, detail=f"You need to spend at least ${promo['min_spend']}.")

    return {
        "message": f"Success! ${promo['discount_value']} discounted.",
        "discount_amount": promo["discount_value"],
        "new_total": subtotal - promo["discount_value"]
    }