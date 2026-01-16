from fastapi import FastAPI

from app.database import engine
from app.models import Base
from app.routers import terms

app = FastAPI()

# Подключение роутеров
app.include_router(terms.router)


@app.get("/")
def read_root():
    return {"message": "Test"}


@app.post("/setup_database")
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    return {"ok": True}
