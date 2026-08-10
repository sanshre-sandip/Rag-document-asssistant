from fastapi import FastAPI
from sqlalchemy import text
from pydantic_settings import BaseSettings
from src.db.database import AsyncSessionLocal
from src.routers.ingestion import router as ingestion_router
from src.routers.chat import router as chat_router


class Settings(BaseSettings):
    app_name: str = "My FastAPI App"


settings = Settings()

app = FastAPI(
    title="My FastAPI App"
)


app.include_router(ingestion_router)
app.include_router(chat_router)

@app.get("/health", tags=["Health"])
async def health_check() -> dict[str, str]:
    return {
        "status": "ok",
        "service": settings.app_name,
    }

@app.get("/health/db", tags=["Health"])
async def database_health() -> dict[str, str]:
    async with AsyncSessionLocal() as session:
        await session.execute(text("SELECT 1"))

    return {
        "status": "ok",
        "database": "postgresql",
    }