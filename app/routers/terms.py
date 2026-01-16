from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from app.database import SessionDep, engine
from app.models import Base, TermModel
from app.schemas import TermAddSchema, TermSchema

router = APIRouter(prefix="/terms", tags=["terms"])


@router.get("/", response_model=list[TermSchema])
async def get_terms(session: SessionDep):
    result = await session.execute(select(TermModel))
    return result.scalars().all()


@router.get("/search/", response_model=list[TermSchema])
async def search_terms(keyword: str, session: SessionDep):
    result = await session.execute(
        select(TermModel).where(
            (TermModel.title.ilike(f"%{keyword}%")) |
            (TermModel.definition.ilike(f"%{keyword}%"))
        )
    )
    return result.scalars().all()


@router.get("/{term_id}", response_model=TermSchema)
async def get_term(term_id: int, session: SessionDep):
    result = await session.execute(select(TermModel).where(TermModel.id == term_id))
    term = result.scalar_one_or_none()
    if term is None:
        raise HTTPException(status_code=404, detail="Термин не найден")
    return term


@router.post("/", response_model=TermSchema)
async def add_term(data: TermAddSchema, session: SessionDep):
    new_term = TermModel(title=data.title, definition=data.definition)
    session.add(new_term)
    await session.commit()
    await session.refresh(new_term)
    return new_term


@router.put("/{term_id}", response_model=TermSchema)
async def update_term(term_id: int, data: TermAddSchema, session: SessionDep):
    term = await session.get(TermModel, term_id)
    if not term:
        raise HTTPException(status_code=404, detail="Термин не найден")
    term.title = data.title
    term.definition = data.definition
    await session.commit()
    await session.refresh(term)
    return term


@router.delete("/{term_id}")
async def delete_term(term_id: int, session: SessionDep):
    term = await session.get(TermModel, term_id)
    if not term:
        raise HTTPException(status_code=404, detail="Термин не найден")
    await session.delete(term)
    await session.commit()
    return {"success": True, "message": "Термин удалён"}
