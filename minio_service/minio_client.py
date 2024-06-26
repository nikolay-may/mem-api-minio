from typing import BinaryIO, Any, Generator
from minio import Minio


class MinioHandler:
    def __init__(
        self,
        minio_endpoint: str,
        access_key: str,
        secret_key: str,
        bucket: str,
        secure: bool = False,
    ) -> None:
        self.client = Minio(
            minio_endpoint,
            access_key,
            secret_key,
            secure=secure,
        )
        self.bucket = bucket

    def upload_file(self, name: str, file: BinaryIO, length: int) -> None:
        return self.client.put_object(self.bucket, name, file, length=length)

    def list_object(self) -> list[Any]:
        object = list(self.client.list_objects(self.bucket))
        return [
            {"name": i.object_name, "last_modified": i.last_modified} for i in object
        ]

    def status_object(self, name: str) -> Any:
        return self.client.stat_object(self.bucket, name)

    def download_file(self, name: str) -> Generator:
        info = self.client.stat_object(self.bucket, name)
        total_size = info.size
        offset = 0

        while True:
            response = self.client.get_object(
                self.bucket,
                name,
                offset=offset,
                length=2048,
            )
            yield response.read()
            offset = offset + 2048
            if offset >= total_size:
                break
