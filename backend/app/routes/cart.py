from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..services.cart_service import CartService
from ..schemas.cart import CartItem, CartItemCreate, CartResponse, CartItemUpdate
from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from typing import Dict


router = APIRouter(
    prefix="/api/cart",
    tags=["cart"]
)


class AddToCartRequest(BaseModel):
    product_id: str = Field(default_factory=lambda: str(uuid4()), 
                description="Product ID", 
                examples=["a0eeb99d-9c0b-4ef8-bb6d-6bb9bd380a11"])
    quantity: int = Field(default=1, gt=0, description="Product Quantity")
    cart: Dict[str, int] = {}

class UpdateCartRequest(BaseModel):
    product_id: str
    quantity: int
    cart: Dict[str, int] = {}

class RemoveFromCartRequest(BaseModel):
    cart: Dict[str, int] = {}


@router.get("/", response_model=CartResponse, status_code=status.HTTP_200_OK)
def get_cart(
    cart_data: Dict[str, int],
    db: Session = Depends(get_db)
):
    service = CartService(db)
    return service.get_cart_details(cart_data=cart_data)

@router.post("/add", status_code=status.HTTP_200_OK)
def add_to_cart(
    request: AddToCartRequest,
    db: Session = Depends(get_db)
):
    service = CartService(db)
    item = CartItemCreate(product_id=request.product_id, quantity=request.quantity)
    updated_cart = service.add_to_cart(request.cart, item=item)
    return {"cart": updated_cart}

@router.put("/update", status_code=status.HTTP_200_OK)
def update_cart(
    request: UpdateCartRequest,
    db: Session = Depends(get_db)
):
    service = CartService(db)
    item = CartItemUpdate(product_id=request.product_id, quantity=request.quantity)
    updated_cart = service.update_cart_item(request.cart, item)
    return {"cart": updated_cart}

@router.delete("/remove/{product_id}", status_code=status.HTTP_200_OK)
def remove_from_cart(
    product_id: str, 
    request: RemoveFromCartRequest,
    db: Session = Depends(get_db)
):
    service = CartService(db)
    updated_cart = service.remove_from_cart(cart_data=request.cart, product_id=product_id)
    return {"cart": updated_cart}
