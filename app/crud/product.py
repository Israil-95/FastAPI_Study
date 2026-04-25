from sqlalchemy.orm import Session
from app.models.models import Product
from app.schemas.product import ProductCreate, ProductUpdate


def get_products(db: Session, search: str = "", category_id: int | None = None):
    query = db.query(Product)

    if category_id is not None:
        query = query.filter(Product.category_id == category_id)

    if search:
        query = query.filter(
            Product.name.contains(search) | Product.description.contains(search)
        )

    return query.all()


def get_product(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()


def create_product(db: Session, product_data: ProductCreate):
    new_product = Product(**product_data.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


def delete_product(db: Session, product_id: int):
    product = get_product(db, product_id)
    if product is None:
        return None

    db.delete(product)
    db.commit()
    return product


def update_product(db: Session, product_id: int, product_data: ProductUpdate):
    product = get_product(db, product_id)
    if product is None:
        return None

    product.name = product_data.name
    product.description = product_data.description
    product.price = product_data.price
    product.category_id = product_data.category_id

    db.commit()
    db.refresh(product)
    return product
