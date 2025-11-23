from uuid import uuid4
from datetime import datetime, timezone


class CategoryFactory:
    """Фабрика для создания категорий"""
    
    @staticmethod
    def create(db, name=None, slug=None):
        """Создаёт категорию и сохраняет в БД"""
        from app.models.category import Category
        
        # ✅ Каждый раз новые значения
        name = name or f"Category{uuid4().hex[:8]}"
        slug = slug or f"slug{uuid4().hex[:8]}"
        
        category = Category(name=name, slug=slug)
        db.add(category)
        db.flush()
        db.refresh(category)
        
        return category


class ProductFactory:
    """Фабрика для создания продуктов"""
    
    @staticmethod
    def create(db, category_id, name=None, description=None, price=None, image_url=None):
        """Создаёт продукт и сохраняет в БД"""
        from app.models.product import Product
        
        # ✅ Генерируем НОВЫЙ UUID для каждого продукта
        product_id = str(uuid4())
        
        name = name or f"Product{uuid4().hex[:8]}"
        description = description or "Test description"
        price = float(price) if price else 99.99
        
        # ✅ ИСПРАВЛЕНИЕ: Используем timezone.utc вместо datetime.UTC
        product = Product(
            id=product_id,
            name=name,
            description=description,
            price=price,
            category_id=category_id,
            image_url=image_url,
            created_at=datetime.now(timezone.utc)  # ✅ Совместимый способ
        )
        db.add(product)
        db.flush()
        db.refresh(product)
        
        return product
