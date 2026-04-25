# python3 -m venv .venv
# python -m venv .venv
# source .venv/bin/activate
# docker compose down
# docker compose up -d
# uvicorn main:app --reload

from fastapi import FastAPI
from database import engine
from app.models.models import Base
from app.api.routers import categories as categories_router, products as products_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI Study")

app.include_router(categories_router.router)
app.include_router(products_router.router)
