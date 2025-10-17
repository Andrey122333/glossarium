from typing import Annotated
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field, ConfigDict

# База данных
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import Mapped, DeclarativeBase, mapped_column

engine = create_async_engine('sqlite+aiosqlite:///./terms.db')
async_session = async_sessionmaker(bind=engine, expire_on_commit=False)

async def get_session():
    async with async_session() as session:
        yield session

SessionDep = Annotated[AsyncSession, Depends(get_session)]

class Base(DeclarativeBase):
    pass

class TermModel(Base):
    __tablename__ = "terms"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    definition: Mapped[str]

app = FastAPI()

class TermAddSchema(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    definition: str = Field(min_length=1)

class TermSchema(TermAddSchema):
    id: int

    class Config:
        orm_mode = True

@app.get("/")
def read_root():
    return {"message": "Test"}

@app.post("/setup_database")
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    return {"ok": True}

@app.get("/terms", response_model=list[TermSchema])
async def get_terms(session: SessionDep):
    result = await session.execute(select(TermModel))
    return result.scalars().all()

@app.get("/terms/{term_id}", response_model=TermSchema)
async def get_term(term_id: int, session: SessionDep):
    result = await session.execute(select(TermModel).where(TermModel.id == term_id))
    term = result.scalar_one_or_none()
    if term is None:
        raise HTTPException(status_code=404, detail="Термин не найден")
    return term

@app.get("/terms/search/", response_model=list[TermSchema])
async def search_terms(keyword: str, session: SessionDep):
    result = await session.execute(
        select(TermModel).where(TermModel.title.ilike(f"%{keyword}%"))
    )
    return result.scalars().all()

@app.post("/terms", response_model=TermSchema)
async def add_term(data: TermAddSchema, session: SessionDep):
    new_term = TermModel(title=data.title, definition=data.definition)
    session.add(new_term)
    await session.commit()
    await session.refresh(new_term)
    return new_term

@app.put("/terms/{term_id}", response_model=TermSchema)
async def update_term(term_id: int, data: TermAddSchema, session: SessionDep):
    term = await session.get(TermModel, term_id)
    if not term:
        raise HTTPException(status_code=404, detail="Термин не найден")
    term.title = data.title
    term.definition = data.definition
    await session.commit()
    await session.refresh(term)
    return term

@app.delete("/terms/{term_id}")
async def delete_term(term_id: int, session: SessionDep):
    term = await session.get(TermModel, term_id)
    if not term:
        raise HTTPException(status_code=404, detail="Термин не найден")
    await session.delete(term)
    await session.commit()
    return {"success": True, "message": "Термин удалён"}
