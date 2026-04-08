from pydantic import BaseModel, Field
from typing import Optional


class RefundRequestBody(BaseModel):
    reason: Optional[str] = Field(default=None, max_length=200)


class RefundResponse(BaseModel):
    order_id: int
    refund_status: str
    message: str
