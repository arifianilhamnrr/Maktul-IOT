from datetime import datetime

from pydantic import BaseModel, ConfigDict


class LedStatusCreate(BaseModel):
    id_device: int
    status_led: bool


class LedStatusRead(LedStatusCreate):
    id: int
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)


class DeviceCreate(BaseModel):
    name: str


class DeviceRead(DeviceCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)
