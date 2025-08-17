from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List

class ProductRequest(BaseModel):
    sku: str = Field(min_length=1, max_length=64)
    name: str = Field(min_length=1, max_length=200)
    price: float = Field(gt=0)
    description: Optional[str] = Field(default=None, max_length=1000)

class ProductResponse(BaseModel):
    id: int
    sku: str
    name: str
    price: str
    description: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class ItemInCart(BaseModel):
    sku: str = Field(min_length=1, max_length=64)
    qty: int = Field(ge=1, le=999)

class QtyInCart(BaseModel):
    qty: int = Field(ge=0, le=999)

class CartLineCons(BaseModel):
    sku: str
    name: str
    unitPrice: str
    qty: int
    lineTotal: str

class CartResponse(BaseModel):
    items: List[CartLineCons]
    subtotal: str
    itemCount: int

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
