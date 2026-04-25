from pydantic import BaseModel, ConfigDict


class CategorySimple(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class CategoryCreate(BaseModel):
    name: str


class CategoryUpdate(BaseModel):
    name: str
