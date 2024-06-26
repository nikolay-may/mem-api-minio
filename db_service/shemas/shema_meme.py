from pydantic import BaseModel


class MemeBase(BaseModel):
    title: str
    description: str

    class Config:
        from_attributes = True


class MemeCreate(MemeBase):
    pass


class MemeAdd(BaseModel):
    id: int


class MemeUpload(BaseModel):
    status: str
    name: str


class MemeResponse(BaseModel):
    meme: MemeAdd
    upload: MemeUpload
