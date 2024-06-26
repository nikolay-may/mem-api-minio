from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from db_service.models import Meme


async def test_session(get_test_async_session: AsyncSession):
    async with get_test_async_session as db_session:
        meme = Meme(title="hehe", description="cat")
        db_session.add(meme)
        await db_session.commit()

        memes_lst_r = await db_session.execute(select(Meme))
        memes_lst = memes_lst_r.scalars().all()
        res = memes_lst[0]
        assert isinstance(res, Meme)
        assert res.title == "hehe"
        assert res.description == "cat"
