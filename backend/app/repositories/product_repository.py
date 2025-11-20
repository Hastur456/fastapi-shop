from sqlalchemy.orm import Session, joinedload
from ..models.product import Product 
from ..schemas.product import ProductCreate

from typing import List
from uuid import UUID


class ProductRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[Product]:
        return self.db.query(Product).options(joinedload(Product.category)).all()

    def get_by_category(self, category_id: int) -> List[Product]:
        return (
            self.db.query(Product)
            .options(joinedload(Product.category))
            .filter(Product.category_id == category_id)
            .all()
        )
    
    def get_by_id(self, product_id: UUID) -> Product | None:
        return (
            self.db.query(Product)
            .options(joinedload(Product.category))
            .filter(Product.id == product_id)
            .one_or_none()
        )
    
    def get_multiple_by_ids(self, product_ids: List[UUID]) -> List[Product]:
        return (
            self.db.query(Product)
            .options(joinedload(Product.category))
            .filter(Product.id.in_(product_ids))
            .all()
        )

    def create(self, product_data: ProductCreate) -> Product | None:
        db_product = Product(**product_data.model_dump())
        self.db.add(db_product)
        self.db.commit()
        self.db.refresh(db_product) 
        return db_product
