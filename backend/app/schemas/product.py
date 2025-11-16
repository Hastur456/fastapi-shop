from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime, timezone
from .category import CategoryResponse
from typing import List
from uuid import uuid4, UUID


class ProductBase(BaseModel):
    name: str = Field(..., min_length=5, max_length=50, description="Product name")
    description: str | None = Field(None, description="Product description")
    price: float = Field(..., gt=0, description="Product price")
    category_id: int = Field(..., description="Category ID")
    image_url: str | None = Field(None, description="Product image URL")


class ProductCreate(ProductBase):
    pass


class ProductResponse(BaseModel):    
    model_config = ConfigDict(from_attributes=True)

    id: UUID = Field(..., description="Product ID")
    name: str
    description: str | None
    price: float
    category_id: int
    image_url: str | None
    create_at: datetime
    category: CategoryResponse = Field(..., description="Product category details")


class ProductListResponse(BaseModel):
    products: List[ProductResponse]
    total: int = Field(..., description="Total products")
