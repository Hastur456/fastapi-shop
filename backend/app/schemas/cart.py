from pydantic import BaseModel, Field
from uuid import UUID


class CardItemBase(BaseModel):
    product_id: UUID = Field(..., description="Product ID")
    quantity: int = Field(..., gt=0, description="Quantity")


class CardItemCreate(CardItemBase):
    pass


class CardItemUpdate(BaseModel):
    product_id: UUID = Field(..., description="Product ID")
    quantity: int = Field(..., gt=0, description="Quantity")


class CardItem(BaseModel):
    product_id: UUID
    name: str = Field(..., description="Product Name")
    price: float = Field(..., description="Product Price")
    quantity: int = Field(..., description="Quantity in card")
    subtotal: float = Field(..., description="Product Price * Quantity")
    image_url: str | None = Field(None, description="Product Name")


class CardResponse(BaseModel):
    items: list[CardItem] = Field(..., description="List of Items in card")
    total: float = Field(..., description="Total card price")
    items_count: int = Field(..., description="Total number of items in card")
    