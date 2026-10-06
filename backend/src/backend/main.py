from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy import select, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import get_session
from backend.models import Device, LedStatus
from backend.schemas import DeviceCreate, DeviceRead, LedStatusCreate, LedStatusRead

app = FastAPI(
    title="LED Test API",
    version="0.1.0",
)


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "LED Test API is running"}


Session = Annotated[AsyncSession, Depends(get_session)]


@app.get("/health")
async def health_check(session: Session) -> dict[str, str]:
    try:
        await session.execute(text("SELECT 1"))
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database is unavailable",
        ) from error
    return {"status": "ok", "database": "connected"}


@app.post(
    "/devices",
    response_model=DeviceRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_device(payload: DeviceCreate, session: Session) -> Device:
    device = Device(name=payload.name)
    session.add(device)
    await session.commit()
    await session.refresh(device)
    return device


@app.get("/devices", response_model=list[DeviceRead])
async def list_devices(session: Session) -> list[Device]:
    result = await session.scalars(select(Device).order_by(Device.id))
    return list(result)


@app.post(
    "/led-statuses",
    response_model=LedStatusRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_led_status(payload: LedStatusCreate, session: Session) -> LedStatus:
    if await session.get(Device, payload.id_device) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device not found",
        )

    led_status = LedStatus(
        id_device=payload.id_device,
        status_led=payload.status_led,
    )
    session.add(led_status)
    await session.commit()
    await session.refresh(led_status)
    return led_status


@app.get("/led-statuses", response_model=list[LedStatusRead])
async def list_led_statuses(session: Session) -> list[LedStatus]:
    result = await session.scalars(
        select(LedStatus).order_by(LedStatus.timestamp.desc(), LedStatus.id.desc())
    )
    return list(result)
