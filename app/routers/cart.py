
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from ..database import SessionLocal
from ..models import Product, CartItem
from ..schemas import ItemInCart, QtyInCart, CartResponse, CartLineCons
from ..dependecy import require_user_auth

router = APIRouter(prefix="/cart", tags=["cart"])

def to_money(value) -> str:
    return f"{value:.2f}"

@router.post("/items")
def add_item(body: ItemInCart, user_name: str = Depends(require_user_auth)):
    with SessionLocal() as db:
        prod = db.execute(select(Product).where(Product.sku==body.sku)).scalar_one_or_none()
        if not prod:
            raise HTTPException(404, "Product not found")
        # upsert add qty
        item = db.execute(select(CartItem).where(CartItem.user_name==user_name, CartItem.sku==body.sku)).scalar_one_or_none()
        if item:
            item.qty += body.qty
        else:
            db.add(CartItem(user_name=user_name, sku=body.sku, qty=body.qty))
        db.commit()
        return {"status":"ok"}

@router.put("/items/{sku}")
def set_item(sku: str, body: QtyInCart, user_name: str = Depends(require_user_auth)):
    with SessionLocal() as db:
        item = db.execute(select(CartItem).where(CartItem.user_name==user_name, CartItem.sku==sku)).scalar_one_or_none()
        if body.qty == 0:
            if item:
                db.delete(item)
                db.commit()
            return {"status":"ok"}
        # ensure product exists
        prod = db.execute(select(Product).where(Product.sku==sku)).scalar_one_or_none()
        if not prod:
            raise HTTPException(404, "Product not found")
        if item:
            item.qty = body.qty
        else:
            db.add(CartItem(user_name=user_name, sku=sku, qty=body.qty))
        db.commit()
        return {"status":"ok"}

@router.delete("/items/{sku}")
def delete_item(sku: str, user_name: str = Depends(require_user_auth)):
    with SessionLocal() as db:
        item = db.execute(select(CartItem).where(CartItem.user_name==user_name, CartItem.sku==sku)).scalar_one_or_none()
        if item:
            db.delete(item)
            db.commit()
        return {"status":"ok"}

@router.get("", response_model=CartResponse)
def get_cart(user_name: str = Depends(require_user_auth)):
    with SessionLocal() as db:
        rows = db.execute(
            select(CartItem.sku, CartItem.qty, Product.name, Product.price)
            .join(Product, Product.sku==CartItem.sku)
            .where(CartItem.user_name==user_name)
        ).all()
        items = []
        subtotal = 0.0
        count = 0
        for sku, qty, name, price in rows:
            unit = float(price)
            line_total = unit * qty
            subtotal += line_total
            count += qty
            items.append(CartLineCons(sku=sku, name=name, unitPrice=to_money(unit), qty=qty, lineTotal=to_money(line_total)))

        return CartResponse(items=items, subtotal=to_money(subtotal), itemCount=count )
