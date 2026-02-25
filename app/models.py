from pydantic import BaseModel
from typing import Optional

class CallResponseData(BaseModel):
    token: str
    channelName: str
    uid: int
    appId: str
    callType: str  # "audio" or "video"

class BaseApiResponse(BaseModel):
    success: bool
    message: str
    data: Optional[dict] = None