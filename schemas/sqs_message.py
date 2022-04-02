import typing as t

from pydantic import BaseModel


class SqsMessage(BaseModel):
    image_key: str
    webhook_url: str
    metadata: t.Union[t.Dict, None]
