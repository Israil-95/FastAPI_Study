from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session
from app.schemas.product import ProductCreate, ProductResponse, ProductUpdate
from database import get_db
from app.crud.product import (
    create_product as create_product_crud,
    delete_product as delete_product_crud,
    get_products,
    update_product as update_product_crud,
)

router = APIRouter(prefix="/api/v1", tags=["products"])

# ПОЛУЧЕНИЕ ПРОДУКТОВ
@router.get("/products", response_model=list[ProductResponse])
def read_products(
    search: str = Query("", description="Search by product name or description"),
    category: int | None = Query(None, description="Filter by category id"),
    db: Session = Depends(get_db),
):
    return get_products(db, search=search, category_id=category)

# ДОАВЛЕНИЕ ПРОДУКТА
@router.post("/products", response_model=ProductResponse)
def create_product(product_data: ProductCreate, db: Session = Depends(get_db)):
    return create_product_crud(db, product_data)

# ИЗМЕНЕНИЕ ПРОДУКТА
@router.put("/products/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    product_data: ProductUpdate,
    db: Session = Depends(get_db),
):
    product = update_product_crud(db, product_id, product_data)
    if product is None:
        raise HTTPException(status_code=404, detail="Товар не найден")
    return product

# УДАЛЕНИЕ ПРОДУКТА
@router.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = delete_product_crud(db, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Товар не найден")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
