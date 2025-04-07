from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.schemas import (
    DeviceCreate,
    DeviceDataCreate,
    DeviceDataResponse,
    DeviceDataStats,
    DeviceOwnerResponse,
    DeviceResponse
)
from core.settings import helper
from api import crud

router = APIRouter()


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_device(
    session: Annotated[AsyncSession, Depends(helper.get_session)],
    data: DeviceCreate | None = None
) -> DeviceResponse:
    if data is not None:
        owner_exists = await crud.check_owner_exists(session, data.owner_id)
        if not owner_exists:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                {'detail': 'Пользователя с таким id не найдено.'}
            )
    return await crud.create_device(session, data)


@router.post('/owners', status_code=status.HTTP_201_CREATED)
async def create_device_owner(
    session: Annotated[AsyncSession, Depends(helper.get_session)]
) -> DeviceOwnerResponse:
    return await crud.create_device_owner(session)


@router.get('/owners/{owner_id}/stats')
async def get_stats_for_device_owner(
    owner_id: int,
    session: Annotated[AsyncSession, Depends(helper.get_session)],
    from_date: datetime | None = None,
    to_date: datetime | None = None
) -> list[DeviceDataStats]:
    return await crud.get_stats_owner_device(
        session, owner_id, from_date, to_date
    )


@router.post('/{device_id}', status_code=status.HTTP_201_CREATED)
async def create_device_data(
    device_id: int,
    data: DeviceDataCreate,
    session: Annotated[AsyncSession, Depends(helper.get_session)]
) -> DeviceDataResponse:
    return await crud.create_data(session, data, device_id)


@router.get('/{device_id}/stats')
async def get_stats(
    device_id: int,
    session: Annotated[AsyncSession, Depends(helper.get_session)],
    from_date: datetime | None = None,
    to_date: datetime | None = None
) -> DeviceDataStats:
    device_exists = await crud.check_device_exists(session, device_id)
    if not device_exists:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            {'detail': 'Устройтсво с таким id не найдено.'}
        )
    result = await crud.get_stats_by_device_id(
        session, device_id, from_date, to_date
    )
    return result
