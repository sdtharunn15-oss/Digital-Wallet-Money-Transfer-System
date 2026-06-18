from pydantic import BaseModel

class MoneyRequest(BaseModel):
    user_id: int
    amount: float


