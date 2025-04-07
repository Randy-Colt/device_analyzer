from datetime import datetime
from typing import Type, Sequence

from pydantic import BaseModel, PositiveInt

from core.settings import Base


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


class Stats(BaseModel):
    min: float
    max: float
    count: int
    sum: float
    median: float


class DeviceDataStats(BaseModel):
    x: Stats
    y: Stats
    z: Stats


def convert_model(
    schema: Type[BaseModel],
    model_objects: Base | Sequence[Base],
    many: bool = False
) -> BaseModel | list[BaseModel]:
    '''Конвертирует модель алхимии в модель пайдентик.'''
    if many:
        return [
            schema.model_validate(model_object, from_attributes=True)
            for model_object in model_objects
        ]
    return schema.model_validate(model_objects, from_attributes=True)
