from sqlalchemy.orm import Session
from ..models.category import Category
from ..schemas.category import CategoryCreate

from typing import List
from uuid import UUID


class CategoryRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[Category]:
        return self.db.query(Category).all()
    
    def get_by_id(self, category_id: UUID) -> Category | None:
        return self.db.query(Category).filter(Category.id == category_id).one_or_none()
    
    def get_by_slug(self, slug: str) -> Category | None:
        return self.db.query(Category).filter(Category.slug == slug).first()
    
    def create(self, category_data: CategoryCreate) -> Category | None:
        db_category = Category(**category_data.model_dump())
        self.db.add(db_category)
        self.db.commit()
        self.db.refresh()
        return db_category
