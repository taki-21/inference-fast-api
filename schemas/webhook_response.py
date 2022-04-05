import typing as t
from enum import Enum

from pydantic import BaseModel


class ResponseStatus(str, Enum):
    success = 'success'
    error = 'error'


class BoxContents(BaseModel):
    box_type: str
    text_box: t.List[int]
    text_cont: str
    text_type: str


class ImageSize(BaseModel):
    width: int
    height: int


class Result(BaseModel):
    img_size: ImageSize
    text: t.List[BoxContents]


class WebHookResponse(BaseModel):
    id: str
    status: ResponseStatus = ResponseStatus.success
    result: t.Union[Result, None]
    message: str
    metadata: t.Optional[t.Dict]


class SavedResult(BaseModel):
    id: str
    result: t.Union[Result, None]
    target_data_s3path: str
