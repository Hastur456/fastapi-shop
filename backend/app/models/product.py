from uuid import uuid4, UUID
from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from ..database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(String, default=str(uuid4()), primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)
    description = Column(Text)
    price = Column(Float, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    image_url = Column(String)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    category = relationship("Category", back_populates="products")

    def __repr__(self):
        return "<Product(id='{}', name='{}', price='{}')>".format(self.id, self.name, self.price)
