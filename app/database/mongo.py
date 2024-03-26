import logging
from typing import List

from beanie import init_beanie
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

from config.settings import settings

logger = logging.getLogger(__name__)


def init_db(app: FastAPI, models: List = None):
    """
    Initialise db connection at startup
    Shutdown the db at shutdown
    :param app: FastAPI to initialise
    :return: None
    """

    @app.on_event("startup")
    async def startup_db_client():
        client = AsyncIOMotorClient(settings.mongo_url)
        app.mongodb_client = client
        await init_beanie(
            database=client[settings.mongo_url.split("/")[-1]], document_models=models or []
        )
        # logger.debug(f"[database] init beanie {mongo_url}, models={models}")

    @app.on_event("shutdown")
    async def shutdown_db_client():
        app.mongodb_client.close()
