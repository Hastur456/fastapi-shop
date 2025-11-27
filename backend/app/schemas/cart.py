from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from typing import List


class CartItemBase(BaseModel):
    product_id: str = Field(default_factory=lambda: str(uuid4()), description="Product ID")
    quantity: int = Field(default=1, gt=0, description="Quantity")


class CartItemCreate(CartItemBase):
    pass


class CartItemUpdate(BaseModel):
    product_id: str = Field(default_factory=lambda: str(uuid4()), description="Product ID")
    quantity: int = Field(default=1, gt=0, description="Quantity")


class CartItem(BaseModel):
    product_id: str = Field(default_factory=lambda: str(uuid4()), description="Product ID")
    name: str = Field(..., description="Product Name")
    price: float = Field(..., description="Product Price")
    quantity: int = Field(default=1, gt=0, description="Quantity in card")
    subtotal: float = Field(..., description="Product Price * Quantity")
    image_url: str | None = Field(None, description="Product Name")


class CartResponse(BaseModel):
    items: list[CartItem] = Field(..., description="List of Items in card")
    total: float = Field(..., description="Total card price")
    items_count: int = Field(..., description="Total number of items in card")
    