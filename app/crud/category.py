from sqlalchemy.orm import Session
from app.models.models import Category
from app.schemas.category import CategoryCreate, CategoryUpdate


def get_categories(db: Session, search: str = "", category_id: int | None = None):
    query = db.query(Category)

    if category_id is not None:
        query = query.filter(Category.id == category_id)

    if search:
        query = query.filter(Category.name.contains(search))

    return query.all()


def get_category(db: Session, category_id: int):
    return db.query(Category).filter(Category.id == category_id).first()


def create_category(db: Session, category_data: CategoryCreate):
    new_category = Category(**category_data.dict())
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category


def delete_category(db: Session, category_id: int):
    category = get_category(db, category_id)
    if category is None:
        return None

    db.delete(category)
    db.commit()
    return category


def update_category(db: Session, category_id: int, category_data: CategoryUpdate):
    category = get_category(db, category_id)
    if category is None:
        return None

    category.name = category_data.name
    db.commit()
    db.refresh(category)
    return category
