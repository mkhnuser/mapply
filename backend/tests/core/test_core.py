import pytest
import asyncio

from aiohttp import web

from logic.app import create_app


async def test_app_start() -> None:
    app_runner = web.AppRunner(create_app())
    await app_runner.setup()
    site = web.TCPSite(app_runner)

    task = asyncio.create_task(site.start())
    await asyncio.sleep(0)
    task.cancel()

    with pytest.raises(asyncio.CancelledError):
        # If there was any application-specific error,
        # It will be reraised during waiting.
        await asyncio.wait_for(task, timeout=None)
