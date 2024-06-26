import datetime
import jwt
from typing import Annotated
from fastapi import APIRouter, File, UploadFile, Form
from starlette.responses import StreamingResponse, JSONResponse
from dateutil.relativedelta import relativedelta
from minio_service.minio_client import MinioHandler
from config_reader import config


router = APIRouter()


minio_handler = MinioHandler(
    config.minio_url,
    config.minio_access_key,
    config.minio_secret_key,
    config.minio_bucket,
    False,
)


@router.post("/upload")
async def upload(file: UploadFile = File(...)):
    minio_handler.upload_file(file.filename, file.file, file.size)
    return {
        "status": "uploaded",
        "name": file.filename,
    }


@router.get("/list")
async def list_object():
    return minio_handler.list_object()


@router.get("/link/{file}")
async def link(file: str):
    obj = minio_handler.status_object(file)
    payload = {
        "filename": obj.object_name,
        "valid_til": str(
            datetime.datetime.now()
            + relativedelta(minutes=(int(config.link_valid_minutes)))
        ),
    }
    encode_jwt = jwt.encode(payload, config.jwt_secret)

    return {"link": f"download/{encode_jwt}"}


@router.get("/download/{temp_link}")
async def download(temp_link: str):
    try:
        decoded_jwt = jwt.decode(temp_link, config.jwt_secret, algorithms=["HS256"])
    except:
        return JSONResponse(
            {"status": "failed", "reason": "Link expired or invalid"}, status_code=400
        )

    valid_til = datetime.datetime.strptime(
        decoded_jwt["valid_til"], "%Y-%m-%d %H:%M:%S.%f"
    )
    if valid_til > datetime.datetime.now():
        filename = decoded_jwt["filename"]
        return StreamingResponse(
            minio_handler.download_file(filename), media_type="application/octet-stream"
        )
    return JSONResponse(
        {"status": "failed", "reason": "Link expired or invalid"}, status_code=400
    )
