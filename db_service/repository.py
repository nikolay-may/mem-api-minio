from typing import List
from sqlalchemy import select
from db_service.models import Meme
from db_service.shemas.shema_meme import MemeBase, MemeAdd
from sqlalchemy.ext.asyncio import AsyncSession


class MemeRepository:
    def __init__(self, async_session: AsyncSession):
        self.ac_session = async_session

    async def add_meme(self, mem: MemeAdd) -> int:
        data = mem.model_dump()
        new_mem = Meme(**data)
        self.ac_session.add(new_mem)
        await self.ac_session.flush()
        await self.ac_session.commit()
        return new_mem.id

    async def get_memes(self, skip: int = 0, limit: int = 10) -> List[Meme]:
        query = select(Meme).offset(skip).limit(limit)
        res = await self.ac_session.execute(query)
        model_meme_lst = res.scalars().all()
        memes = [MemeBase.model_validate(model_meme) for model_meme in model_meme_lst]
        return memes

    async def get_meme(self, id_meme: int) -> Meme:
        query = select(Meme).where(Meme.id == id_meme)
        res = await self.ac_session.execute(query)
        meme_model = res.scalar()
        if meme_model:
            return meme_model
        return None

    async def update_meme(self, id_meme, update_meme: MemeBase) -> bool:
        query = select(Meme).where(Meme.id == id_meme)
        res = await self.ac_session.execute(query)
        meme_model = res.scalar()
        if meme_model:
            meme_model.title = update_meme.title
            meme_model.description = update_meme.description
            await self.ac_session.commit()
            await self.ac_session.refresh(meme_model)
            return MemeBase.model_validate(meme_model)
        return False

    async def delete_meme(self, id_meme: int) -> bool:
        query = select(Meme).where(Meme.id == id_meme)
        res = await self.ac_session.execute(query)
        meme_model = res.scalar()
        if meme_model:
            await self.ac_session.delete(meme_model)
            await self.ac_session.commit()
            return True
        return False
