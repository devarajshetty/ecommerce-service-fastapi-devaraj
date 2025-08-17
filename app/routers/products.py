
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models import Product
from ..schemas import ProductRequest, ProductResponse
from ..dependecy import require_admin_auth


router = APIRouter(prefix="/products", tags=["products"])

def to_money(value) -> str:
    return f"{value:.2f}"

@router.get("", response_model=dict)
def list_products(
    search: str | None = Query(None),
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
):
    with SessionLocal() as db:
        stmt = select(Product)
        total = db.execute(select(func.count()).select_from(stmt.subquery())).scalar_one()
        items = db.execute(stmt.order_by(Product.id).offset((page-1)*size).limit(size)).scalars().all()
        out = [ProductResponse.model_validate({"id": p.id, "sku": p.sku, "name": p.name, "price": to_money(p.price)}) for p in items]
        return {"items": out, "page": page, "page_size": size, "total": total}

@router.post("", response_model=ProductResponse, dependencies=[Depends(require_admin_auth)])
def create_product(body: ProductRequest):
    with SessionLocal() as db:
        p = Product(sku=body.sku, name=body.name, price=body.price)
        db.add(p)
        try:
            db.commit()
        except Exception:
            db.rollback()
            raise HTTPException(400, "SKU already exists or invalid")
        db.refresh(p)
        return ProductResponse.model_validate({"id": p.id, "sku": p.sku, "name": p.name, "price": to_money(p.price)})

@router.put("/{product_id}", response_model=ProductResponse, dependencies=[Depends(require_admin_auth)])
def update_product(product_id: int, body: ProductRequest):
    with SessionLocal() as db:
        p = db.get(Product, product_id)
        if not p:
            raise HTTPException(404, "Product not found")
        p.sku, p.name, p.price = body.sku, body.name, body.price
        try:
            db.commit()
        except Exception:
            db.rollback()
            raise HTTPException(400, "SKU already exists or invalid")
        db.refresh(p)
        return ProductResponse.model_validate({"id": p.id, "sku": p.sku, "name": p.name, "price": to_money(p.price)})

@router.delete("/{product_id}", dependencies=[Depends(require_admin_auth)])
def delete_product(product_id: int):
    with SessionLocal() as db:
        p = db.get(Product, product_id)
        if not p:
            raise HTTPException(404, "Product not found")
        db.delete(p)
        db.commit()
        return {"status":"deleted"}
