from datetime import datetime
from sqlalchemy import exists, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.selectable import Select

from api.schemas import DeviceCreate, DeviceDataCreate
from core.models import Device, DeviceData, DeviceOwner


async def create_device(
    session: AsyncSession,
    data: DeviceCreate
) -> Device:
    if data is not None:
        device = Device(**data.model_dump())
    else:
        device = Device()
    session.add(device)
    await session.commit()
    await session.refresh(device)
    return device


async def create_data(
    session: AsyncSession,
    data: DeviceDataCreate,
    device_id: int
) -> DeviceData:
    dev_data = DeviceData(device_id=device_id, **data.model_dump())
    session.add(dev_data)
    await session.commit()
    await session.refresh(dev_data)
    return dev_data


async def create_device_owner(session: AsyncSession) -> DeviceOwner:
    owner = DeviceOwner()
    session.add(owner)
    await session.commit()
    await session.refresh(owner)
    return owner


async def check_device_exists(
    session: AsyncSession,
    device_id: int
) -> bool:
    return await session.scalar(
        exists().where(Device.id == device_id).select()
    )


def get_query_stats(
    from_date: datetime | None,
    to_date: datetime | None
) -> Select:
    aggregations = (
        func.min(DeviceData.x).label('x_min'),
        func.min(DeviceData.y).label('y_min'),
        func.min(DeviceData.z).label('z_min'),
        func.max(DeviceData.x).label('x_max'),
        func.max(DeviceData.y).label('y_max'),
        func.max(DeviceData.z).label('z_max'),
        func.percentile_cont(0.5).within_group(DeviceData.x).label('x_median'),
        func.percentile_cont(0.5).within_group(DeviceData.y).label('y_median'),
        func.percentile_cont(0.5).within_group(DeviceData.z).label('z_median'),
        func.count(func.distinct(DeviceData.id)).label('total_count')
    )
    query = (
        select(DeviceData.device_id, *aggregations)
        .group_by(DeviceData.device_id)
    )
    if from_date is not None:
        query = query.where(DeviceData.timestamp >= from_date)
    if to_date is not None:
        query = query.where(DeviceData.timestamp <= to_date)
    return query


async def get_stats_by_device_id(
    session: AsyncSession,
    device_id: int,
    from_date: datetime | None,
    to_date: datetime | None
):
    query = get_query_stats(from_date, to_date)
    query = query.where(DeviceData.device_id == device_id)
    result = await session.execute(query)
    return result.mappings().one()


async def get_stats_owner_device(
    session: AsyncSession,
    owner_id: int,
    from_date: datetime | None,
    to_date: datetime | None
):
    query = get_query_stats(from_date, to_date)
    query = (
        query.where(Device.owner_id == owner_id)
        .join(Device, DeviceData.device_id == Device.id)
    )
    result = await session.execute(query)
    return result.mappings().all()
