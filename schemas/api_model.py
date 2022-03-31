import typing as t

from pydantic import BaseModel


class ApiModel(BaseModel):
    drawing_pdf_data: str
    webhook_url: str
    metadata: t.Union[t.Dict, None]
