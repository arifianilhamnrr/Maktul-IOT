from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database import Base


class Device(Base):
    __tablename__ = "devices"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    led_statuses: Mapped[list["LedStatus"]] = relationship(
        back_populates="device",
    )


class LedStatus(Base):
    __tablename__ = "led_statuses"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_device: Mapped[int] = mapped_column(
        ForeignKey("devices.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    status_led: Mapped[bool] = mapped_column(Boolean, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.current_timestamp(),
    )
    device: Mapped[Device] = relationship(back_populates="led_statuses")
