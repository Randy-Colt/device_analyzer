from datetime import datetime

from pydantic import BaseModel, NonNegativeInt, PositiveInt


class BaseDevice(BaseModel):
    owner_id: PositiveInt | None = None


class DeviceCreate(BaseDevice):
    pass


class DeviceResponse(BaseDevice):
    id: PositiveInt


class BaseDeviceData(BaseModel):
    x: float
    y: float
    z: float


class DeviceDataCreate(BaseDeviceData):
    pass


class DeviceDataResponse(BaseDeviceData):
    device_id: PositiveInt
    timestamp: datetime


class DeviceDataStats(BaseModel):
    device_id: PositiveInt
    x_min: float
    y_min: float
    z_min: float
    x_max: float
    y_max: float
    z_max: float
    x_median: float
    y_median: float
    z_median: float
    total_count: NonNegativeInt


class BaseDeviceOwner(BaseModel):
    pass


class DeviceOwnerCreate(BaseDeviceOwner):
    pass


class DeviceOwnerResponse(BaseDeviceOwner):
    id: PositiveInt
