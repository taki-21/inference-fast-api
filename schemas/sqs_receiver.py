from pydantic import BaseModel


class SqsReceiverOut(BaseModel):
    status: str
