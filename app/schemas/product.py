from pydantic import BaseModel, ConfigDict
from app.schemas.category import CategorySimple


class ProductBase(BaseModel):
    name: str
    description: str
    price: int
    category_id: int


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    pass


class ProductResponse(ProductBase):
    id: int
    category: CategorySimple

    model_config = ConfigDict(from_attributes=True)
