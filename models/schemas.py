from typing import Dict, Any, Optional
from pydantic import BaseModel, Field


class BaseResponse(BaseModel):
    status: str
    message: str
    data: Optional[Dict[str, Any]] = None


class SOSData(BaseModel):
    sos_text: str
    phone_number: str = Field(regex="^\+91[1-9]\d{9}$")


class ResponderResponse(BaseModel):
    sos_id: str
    response: str = Field(regex="^(accept|decline)$")
