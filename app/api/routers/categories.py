from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session
from app.schemas.category import CategoryCreate, CategorySimple, CategoryUpdate
from database import get_db
from app.crud.category import (
    create_category as create_category_crud,
    delete_category as delete_category_crud,
    get_categories,
    update_category as update_category_crud,
)

router = APIRouter(prefix="/api/v1", tags=["categories"])

# ПОЛУЧЕНИЕ КАТЕГОРИЙ
@router.get("/categories", response_model=list[CategorySimple])
def read_categories(
    search: str = Query("", description="Search by category name"),
    category: int | None = Query(None, description="Filter by category id"),
    db: Session = Depends(get_db),
):
    return get_categories(db, search=search, category_id=category)

# ДОАВЛЕНИЕ КАТЕГОРИИ
@router.post("/categories", response_model=CategorySimple)
def create_category(category_data: CategoryCreate, db: Session = Depends(get_db)):
    return create_category_crud(db, category_data)

# ИЗМЕНЕНИЕ КАТЕГОРИИ
@router.put("/categories/{category_id}", response_model=CategorySimple)
def update_category(
    category_id: int,
    category_data: CategoryUpdate,
    db: Session = Depends(get_db),
):
    category = update_category_crud(db, category_id, category_data)
    if category is None:
        raise HTTPException(status_code=404, detail="Категория не найдена")
    return category

# УДАЛЕНИЕ КАТЕГОРИИ
@router.delete("/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    category = delete_category_crud(db, category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Категория не найдена")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
