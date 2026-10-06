import asyncio

from httpx import ASGITransport, AsyncClient
from sqlalchemy import delete

from backend.database import SessionLocal
from backend.main import app
from backend.models import Device, LedStatus


async def main() -> None:
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        health = await client.get("/health")
        device = await client.post("/devices", json={"name": "Smoke Test Device"})
        device.raise_for_status()
        created = await client.post(
            "/led-statuses",
            json={"id_device": device.json()["id"], "status_led": True},
        )
        missing_device = await client.post(
            "/led-statuses",
            json={"id_device": 2_147_483_647, "status_led": False},
        )
        statuses = await client.get("/led-statuses")

    health.raise_for_status()
    created.raise_for_status()
    statuses.raise_for_status()
    assert missing_device.status_code == 404

    created_status = created.json()
    assert any(item["id"] == created_status["id"] for item in statuses.json())
    print(health.json())
    print(created_status)

    async with SessionLocal() as session:
        await session.execute(
            delete(LedStatus).where(LedStatus.id == created_status["id"])
        )
        await session.execute(delete(Device).where(Device.id == device.json()["id"]))
        await session.commit()


if __name__ == "__main__":
    asyncio.run(main())
