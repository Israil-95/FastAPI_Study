# python3 -m venv .venv
# python -m venv .venv
# source .venv/bin/activate
# uvicorn main:app --reload
'''
GET POST PUT,PATCH,DELETE,OPTIONS

GET - для получения данных
POST - для добавления данных (добавление товара в корзину, регистрация аккаунта)
GET - данные передаются только через URL 
https://api.myshop.com/api/v1/category/laptops/products?price_from=10000&brand=xiaomi
POST данные можно отправить через тело запроса
POST https://api.myshop.com/api/v1/auth/register
{
    "login":"ali_123",
    "password":"password_123"
}
PUT - запрос на изменение сущности
PATCH- запрос на частичное изменение сущности
DELETE - запрос на удаление сущности

http://localhost:3003
'''

from typing import Annotated
from fastapi import FastAPI, Path, Query,Response,status,Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db
import models
from database import engine

app = FastAPI()

'''
/products?a=b&c=d
/product/{id}
/categories/
/categories/{id}/products
'''

products = [
  {
    "id": 1,
    "name": "Smartphone X12",
    "description": "A powerful smartphone with a 6.5-inch display and 128GB storage.",
    "category_id": 1
  },

  {
    "id": 2,
    "name": "Wireless Headphones",
    "description": "Noise-cancelling over-ear headphones with 30-hour battery life.",
    "category_id": 1
  },

  {
    "id": 3,
    "name": "Laptop Pro 15",
    "description": "High-performance laptop with 16GB RAM and 512GB SSD.",
    "category_id": 1
  },

  {
    "id": 4,
    "name": "Men's Running Jacket",
    "description": "Lightweight and water-resistant jacket for outdoor running.",
    "category_id": 2
  },

  {
    "id": 5,
    "name": "Women's Summer Dress",
    "description": "Elegant floral dress made from 100% breathable cotton.",
    "category_id": 2
  },

  {
    "id": 6,
    "name": "Garden Hose 20m",
    "description": "Durable expandable garden hose with spray nozzle included.",
    "category_id": 3
  },

  {
    "id": 7,
    "name": "Ceramic Flower Pot Set",
    "description": "Set of 3 decorative ceramic pots in various sizes.",
    "category_id": 3
  },

  {
    "id": 8,
    "name": "Yoga Mat",
    "description": "Non-slip eco-friendly yoga mat, 6mm thick.",
    "category_id": 4
  },

  {
    "id": 9,
    "name": "Mountain Bike Helmet",
    "description": "Certified safety helmet with ventilation system and adjustable fit.",
    "category_id": 4
  },

  {
    "id": 10,
    "name": "JavaScript: The Good Parts",
    "description": "A concise guide to the best features of the JavaScript language.",
    "category_id": 5
  },

  {
    "id": 11,
    "name": "Clean Code",
    "description": "A handbook of agile software craftsmanship by Robert C. Martin.",
    "category_id": 5
  }
]

categories = [
  {
    "id": 1,
    "name": "Electronics"
  },

  {
    "id": 2,
    "name": "Clothing"
  },

  {
    "id": 3,
    "name": "Home & Garden"
  },

  {
    "id": 4,
    "name": "Sports & Outdoors"
  },

  {
    "id": 5,
    "name": "Books"
  }
]

class CategorySimple(BaseModel):
    id: int
    name: str
    class Config:
        from_attributes = True

class ProductResponse(BaseModel):
    id: int
    name: str 
    description: str
    price: int 
    category: CategorySimple
    class Config:
       from_attributes = True

@app.get("/api/v1/products", response_model = list[ProductResponse])
async def get_products(
    search: str = "", 
    category: str = "", 
    db: Session = Depends(get_db)
):
    # 1. Вместо result = products (твой начальный список)
    result = db.query(models.Product) 

    # 2. Твое условие с категорией
    if category != "":
        # Это ЗАМЕНЯЕТ твой [product for product in result if ...]
        # Мы говорим базе: "Оставь только те, где ID совпадает"
        result = result.filter(models.Product.category_id == int(category))

    # 3. Твое условие с поиском
    if search != "":
        # Это ЗАМЕНЯЕТ твой поиск внутри цикла
        result = result.filter(
            models.Product.name.contains(search) | 
            models.Product.description.contains(search)
        )

    # 4. В самом конце выполняем запрос и отдаем список (как твой return)
    return result.all()

@app.get("/api/v1/categories")
async def get_categories(
    search: str = "", 
    category: str = "", 
    db: Session = Depends(get_db)
):
    result = db.query(models.Category)

    if category != "":
        result = result.filter(models.Category.id == int(category))

    if search != "":
        result = result.filter(models.Category.name.contains(search))

    return result.all()

class CategoryCreate(BaseModel):
    name: str 
  
class CategoryUpdate(BaseModel):
    name: str

# СОЗДАНИЕ КАТЕГОРИИ
@app.post("/api/v1/categories")
async def create_category(category_data: CategoryCreate, db: Session = Depends(get_db)):
    new_category = models.Category(name = category_data.name)    

    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return {"status": "success", "data": new_category}

# Схема для создания товара         
class ProductCreate(BaseModel):
    name: str
    description: str
    price: int
    category_id: int

class ProductUpdate(BaseModel):
    name: str
    description: str
    price: int
    category_id: int

# СОЗДАНИЕ ТОВАРА
@app.post("/api/v1/products")
async def create_product(product_data: ProductCreate, db: Session = Depends(get_db)):
    new_product = models.Product(
        name=product_data.name,
        description=product_data.description,
        price=product_data.price,
        category_id=product_data.category_id
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return {"status": "success", "data": new_product}

#  УДАЛЕНИЕ КАТЕГОРИИ 
@app.delete("/api/v1/categories/{category_id}")
async def delete_category(category_id: int, db: Session = Depends(get_db)):
    
    category = db.query(models.Category).filter(models.Category.id == category_id).first()

    if category is None:
        return {"Error": "Категория не найдена"}
    
    db.delete(category)
    db.commit()

    return {"status": "success", "message": f"Категория с ID {category_id} удалена"}

#  УДАЛЕНИЕ ПРОДУКТА
@app.delete("/api/v1/products/{products_id}")
async def delete_products(products_id: int, db: Session = Depends(get_db)):
    
    products = db.query(models.Product).filter(models.Product.id == products_id).first()

    if products is None:
        return {"Error": "Товар не найдена"}
    
    db.delete(products)
    db.commit()

    return {"status": "success", "message": f"Товар с ID {products_id} удалена"}

# ИЗМЕНЕНИЕ КАТЕГОРИИ
@app.put("/api/v1/categories/{category_id}")
async def update_category(category_id: int, category_data: CategoryUpdate,  db: Session = Depends(get_db)):
    
    category = db.query(models.Category).filter(models.Category.id == category_id).first()

    if category is None:
        return {"Error": "Категория не найдена"}
    
    category.name = category_data.name 

    db.commit()
    db.refresh(category)

    return {category}

# ИЗМЕНЕНИЕ ПРОДУКТА
@app.put("/api/v1/products/{products_id}")
async def update_products(products_id: int, product_data: ProductUpdate, db: Session = Depends(get_db)):
    
    products = db.query(models.Product).filter(models.Product.id == products_id).first()

    if products is None:
        return {"Error": "Товар не найден"}
    
    products.name = product_data.name
    products.description = product_data.description
    products.price = product_data.price
    products.category_id = product_data.category_id
    
    db.commit()
    db.refresh(products)

    return {products}