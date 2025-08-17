from sqlalchemy import Numeric, UniqueConstraint, ForeignKey, Column, Integer, String, Enum
from .database import Base
import enum

class RoleEnum(str, enum.Enum):
    admin = "admin"
    user = "user"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    role = Column(Enum(RoleEnum), nullable=False, default=RoleEnum.user)

    
class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    sku = Column(String(64), unique=True, index=True,  nullable=False)
    name = Column(String(200),  nullable=False)
    price = Column(Numeric(10,2), nullable=False)

class CartItem(Base):
    __tablename__ = "cart_items"
    id= Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String(128), index=True)
    sku = Column(String(64), ForeignKey("products.sku"))
    qty = Column(Integer)

    __table_args__ = (UniqueConstraint("user_name", "sku", name="uq_cart_user_sku"),)
