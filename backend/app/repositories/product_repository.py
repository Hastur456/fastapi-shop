from sqlalchemy.orm import Session
from ..models.product import Product 
from ..schemas.product import ProductCreate

from typing import List
from uuid import UUID


class CategoryRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[Product]:
        return self.db.query(Product).all()
    
    def get_by_id(self, Product_id: UUID) -> Product | None:
        return self.db.query(Product).filter(Product.id == Product_id).one_or_none()
    
    def get_by_slug(self, slug: str) -> Product | None:
        return self.db.query(Product).filter(Product.slug == slug).first()
    
    def create(self, Product_data: ProductCreate) -> Product | None:
        db_Product = Product(**Product_data.model_dump())
        self.db.add(db_Product)
        self.db.commit()
        self.db.refresh()
        return db_Product
