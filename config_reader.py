from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr, Field
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    db_url: SecretStr
    minio_url: str = Field(validation_alias="minio_url")
    minio_access_key: str = Field(validation_alias="minio_access_key")
    minio_secret_key: str = Field(validation_alias="minio_secret_key")
    minio_bucket: str = Field(validation_alias="minio_bucket")
    link_valid_minutes: str = Field(validation_alias="link_valid_minutes")
    jwt_secret: str = Field(validation_alias="jwt_secret")

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


config = Settings()
