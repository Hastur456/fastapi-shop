import pytest
from sqlalchemy.orm import Session


@pytest.mark.unit
class TestProductService:
    """Тесты ProductService"""
    
    def test_get_all_products_empty(self, db: Session):
        """Все продукты пусто"""
        from app.services.product_service import ProductService
        
        service = ProductService(db)
        result = service.get_all_products()
        
        # result это объект ProductListResponse
        assert result.total == 0
        assert len(result.products) == 0
    
    def test_get_all_products_with_data(self, db: Session):
        """Все продукты с данными"""
        from app.services.product_service import ProductService
        from tests.factories import CategoryFactory, ProductFactory
        
        cat = CategoryFactory.create(db)
        ProductFactory.create(db, category_id=cat.id, name="Prod1")
        ProductFactory.create(db, category_id=cat.id, name="Prod2")
        
        service = ProductService(db)
        result = service.get_all_products()
        
        # Используем атрибуты объекта, не dict
        assert result.total == 2
        assert len(result.products) == 2
    
    def test_get_product_by_id(self, db: Session):
        """Получение продукта по ID"""
        from app.services.product_service import ProductService
        from tests.factories import CategoryFactory, ProductFactory
        
        cat = CategoryFactory.create(db)
        prod = ProductFactory.create(db, category_id=cat.id, name="Test", price=99.99)
        
        service = ProductService(db)
        result = service.get_product_by_id(str(prod.id))
        
        assert result.id == prod.id
        assert result.name == "Test"
    
    def test_get_products_by_category(self, db: Session):
        """Продукты по категории"""
        from app.services.product_service import ProductService
        from tests.factories import CategoryFactory, ProductFactory
        
        cat1 = CategoryFactory.create(db, name="Electronics")
        cat2 = CategoryFactory.create(db, name="Books")
        
        ProductFactory.create(db, category_id=cat1.id, name="Laptop")
        ProductFactory.create(db, category_id=cat1.id, name="Phone")
        ProductFactory.create(db, category_id=cat2.id, name="Book")
        
        service = ProductService(db)
        result = service.get_products_by_category(cat1.id)
        
        # result это объект ProductListResponse
        assert result.total == 2


@pytest.mark.unit
class TestCategoryService:
    """Тесты CategoryService"""
    
    def test_get_all_categories_empty(self, db: Session):
        """Все категории пусто"""
        from app.services.category_service import CategoryService
        
        service = CategoryService(db)
        result = service.get_all_categories()
        
        assert result == []
    
    def test_get_all_categories_with_data(self, db: Session):
        """Все категории с данными"""
        from app.services.category_service import CategoryService
        from tests.factories import CategoryFactory
        
        CategoryFactory.create(db, name="Electronics", slug="electronics")
        CategoryFactory.create(db, name="Books", slug="books")
        
        service = CategoryService(db)
        result = service.get_all_categories()
        
        assert len(result) == 2
    
    def test_get_category_by_id(self, db: Session):
        """Получение категории по ID"""
        from app.services.category_service import CategoryService
        from tests.factories import CategoryFactory
        
        cat = CategoryFactory.create(db, name="Test", slug="test")
        
        service = CategoryService(db)
        result = service.get_category_by_id(cat.id)
        
        # result это объект CategoryResponse
        assert result.id == cat.id
        assert result.name == "Test"
        assert result.slug == "test"


@pytest.mark.unit
class TestCartService:
    """Тесты CartService"""
    
    def test_add_to_cart(self, db: Session):
        """Добавление в корзину"""
        from app.services.cart_service import CartService
        from app.schemas.cart import CartItemCreate
        from tests.factories import CategoryFactory, ProductFactory
        
        cat = CategoryFactory.create(db)
        prod = ProductFactory.create(db, category_id=cat.id)
        
        service = CartService(db)
        item = CartItemCreate(product_id=str(prod.id), quantity=2)
        cart = service.add_to_cart({}, item=item)
        
        assert str(prod.id) in cart
        assert cart[str(prod.id)] == 2
    
    def test_add_to_cart_update_qty(self, db: Session):
        """Повторное добавление увеличивает количество"""
        from app.services.cart_service import CartService
        from app.schemas.cart import CartItemCreate
        from tests.factories import CategoryFactory, ProductFactory
        
        cat = CategoryFactory.create(db)
        prod = ProductFactory.create(db, category_id=cat.id)
        
        service = CartService(db)
        
        item1 = CartItemCreate(product_id=str(prod.id), quantity=1)
        cart = service.add_to_cart({}, item=item1)
        assert cart[str(prod.id)] == 1
        
        item2 = CartItemCreate(product_id=str(prod.id), quantity=2)
        cart = service.add_to_cart(cart, item=item2)
        assert cart[str(prod.id)] == 3
    
    def test_remove_from_cart(self, db: Session):
        """Удаление из корзины"""
        from app.services.cart_service import CartService
        from tests.factories import CategoryFactory, ProductFactory
        
        cat = CategoryFactory.create(db)
        prod = ProductFactory.create(db, category_id=cat.id)
        
        service = CartService(db)
        cart = service.remove_from_cart({str(prod.id): 2}, str(prod.id))
        
        assert str(prod.id) not in cart
    
    def test_get_cart_details(self, db: Session):
        """Детали корзины"""
        from app.services.cart_service import CartService
        from tests.factories import CategoryFactory, ProductFactory
        
        cat = CategoryFactory.create(db)
        prod = ProductFactory.create(db, category_id=cat.id, name="Item", price=50.0)
        
        service = CartService(db)
        result = service.get_cart_details({str(prod.id): 2})
        
        # result это объект CartResponse с атрибутами items и total
        assert len(result.items) == 1
        assert result.total == 100.0
