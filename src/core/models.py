from datetime import datetime

from sqlalchemy import ForeignKey, func, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.settings import Base


class Device(Base):

    __tablename__ = 'devices'

    owner_id: Mapped[int | None] = mapped_column(
        ForeignKey('device_owners.id')
    )
    characteristics: Mapped[list['DeviceData']] = relationship(
        back_populates='device',
        lazy='joined'
    )
    owner: Mapped['DeviceOwner'] = relationship(
        back_populates='device',
        lazy='joined'
    )


class DeviceData(Base):

    __tablename__ = 'device_data'

    device: Mapped[Device] = relationship(
        back_populates='characteristics',
        lazy='joined'
    )
    device_id: Mapped[int] = mapped_column(ForeignKey('devices.id'))
    x: Mapped[float]
    y: Mapped[float]
    z: Mapped[float]
    timestamp: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now()
    )


class DeviceOwner(Base):

    __tablename__ = 'device_owners'

    device: Mapped[list[Device]] = relationship(
        back_populates='owner',
        lazy='joined'
    )
