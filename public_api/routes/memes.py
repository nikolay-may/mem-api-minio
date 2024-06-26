from fastapi import APIRouter, Depends, Form, HTTPException, UploadFile, File
from typing import List, Annotated
from db_service.shemas import shema_meme
from db_service.db_init import get_async_session
from db_service.repository import MemeRepository
from minio_service.main import upload
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


def get_meme_repository(
    session: AsyncSession = Depends(get_async_session),
) -> MemeRepository:
    return MemeRepository(session)


@router.get("/memes", response_model=List[shema_meme.MemeBase])
async def get_memes(
    skip: int = 0,
    limit: int = 10,
    repository: MemeRepository = Depends(get_meme_repository),
):
    memes = await repository.get_memes(skip=skip, limit=limit)
    if not memes:
        raise HTTPException(status_code=404, detail="Memes not found")
    return memes


@router.get("/meme/{id}", response_model=shema_meme.MemeBase)
async def get_meme(
    id: int, repository: MemeRepository = Depends(get_meme_repository)
) -> shema_meme.MemeBase:
    meme = await repository.get_meme(id_meme=id)
    if not meme:
        raise HTTPException(status_code=404, detail="Meme not found")
    return shema_meme.MemeBase.model_validate(meme)


@router.post("/meme", response_model=shema_meme.MemeResponse)
async def upload_meme(
    title: Annotated[str, Form()],
    description: Annotated[str, Form()],
    file: Annotated[UploadFile, File()],
    upload_response: dict = Depends(upload),
    repository: MemeRepository = Depends(get_meme_repository),
) -> shema_meme.MemeResponse:
    meme_data = shema_meme.MemeBase(title=title, description=description)
    upload_meme_id = await repository.add_meme(meme_data)
    meme_add = shema_meme.MemeAdd(id=upload_meme_id)
    meme_upload = shema_meme.MemeUpload(**upload_response)
    return shema_meme.MemeResponse(meme=meme_add, upload=meme_upload)


@router.put("/memes/{id}", response_model=shema_meme.MemeBase)
async def update_meme(
    id: int,
    meme: shema_meme.MemeBase,
    repository: MemeRepository = Depends(get_meme_repository),
):
    updated_meme = await repository.update_meme(id_meme=id, update_meme=meme)
    if not updated_meme:
        raise HTTPException(status_code=404, detail="Meme not found")
    return updated_meme


@router.delete("/memes/{id}", response_model=dict)
async def delete_meme(
    id: int, repository: MemeRepository = Depends(get_meme_repository)
):
    deleted = await repository.delete_meme(id_meme=id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Meme not found")
    return {"detail": "Meme deleted successfully"}
