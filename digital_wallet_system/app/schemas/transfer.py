from pydantic import BaseModel


class TransferRequest(BaseModel):

    sender_user_id: int

    receiver_user_id: int

    amount: float