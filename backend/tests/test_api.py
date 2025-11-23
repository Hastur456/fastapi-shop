import pytest
from fastapi.testclient import TestClient


@pytest.mark.api
class TestProductsAPI:
    """Тесты Products API"""
    
    def test_get_products_empty(self, client: TestClient):
        """Получение пустого списка продуктов"""
        response = client.get("/api/products/")
        assert response.status_code == 200
    
    def test_get_products_with_data(self, client: TestClient, db):
        """Получение продуктов с данными"""
        from tests.factories import CategoryFactory, ProductFactory
        
        cat = CategoryFactory.create(db)
        ProductFactory.create(db, category_id=cat.id, name="Laptop")
        ProductFactory.create(db, category_id=cat.id, name="Mouse")
        
        response = client.get("/api/products/")
        assert response.status_code == 200
        data = response.json()
        assert len(data["products"]) >= 2
    
    def test_get_product_by_id(self, client: TestClient, db):
        """Получение продукта по ID"""
        from tests.factories import CategoryFactory, ProductFactory
        
        cat = CategoryFactory.create(db)
        prod = ProductFactory.create(db, category_id=cat.id, name="TestProd")
        
        response = client.get(f"/api/products/{prod.id}")
        assert response.status_code == 200
        assert response.json()["name"] == "TestProd"
    
    def test_get_product_not_found(self, client: TestClient):
        """Несуществующий продукт"""
        response = client.get("/api/products/00000000-0000-0000-0000-000000000000")
        assert response.status_code == 404
    
    def test_get_products_by_category(self, client: TestClient, db):
        """Продукты по категории"""
        from tests.factories import CategoryFactory, ProductFactory
        
        cat = CategoryFactory.create(db, name="Electronics")
        ProductFactory.create(db, category_id=cat.id, name="Laptop")
        ProductFactory.create(db, category_id=cat.id, name="Phone")
        
        response = client.get(f"/api/products/category/{cat.id}")
        assert response.status_code == 200
        assert response.json()["total"] == 2


@pytest.mark.api
class TestCategoriesAPI:
    """Тесты Categories API"""
    
    def test_get_categories_empty(self, client: TestClient):
        """Пустой список категорий"""
        response = client.get("/api/categories/")
        assert response.status_code == 200
    
    def test_get_categories_with_data(self, client: TestClient, db):
        """Категории с данными"""
        from tests.factories import CategoryFactory
        
        CategoryFactory.create(db, name="Electronics", slug="electronics")
        CategoryFactory.create(db, name="Books", slug="books")
        
        response = client.get("/api/categories/")
        assert response.status_code == 200
        assert len(response.json()) >= 2
    
    def test_get_category_by_id(self, client: TestClient, db):
        """Категория по ID"""
        from tests.factories import CategoryFactory
        
        cat = CategoryFactory.create(db, name="TestCat", slug="testcat")
        
        response = client.get(f"/api/categories/{cat.id}")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "TestCat"
    
    def test_get_category_not_found(self, client: TestClient):
        """Несуществующая категория"""
        response = client.get("/api/categories/999999")
        assert response.status_code == 404


@pytest.mark.api
class TestCartAPI:
    """Тесты Cart API"""
    
    def test_get_empty_cart(self, client: TestClient):
        """Пустая корзина"""
        response = client.get("/api/cart/")
        assert response.status_code == 200
    
    def test_add_to_cart(self, client: TestClient, db):
        """Добавление в корзину"""
        from tests.factories import CategoryFactory, ProductFactory
        
        cat = CategoryFactory.create(db)
        prod = ProductFactory.create(db, category_id=cat.id, price=100.0)
        
        response = client.post(
            "/api/cart/add",
            json={"product_id": str(prod.id), "quantity": 2, "cart": {}}
        )
        assert response.status_code == 200
    
    def test_update_cart(self, client: TestClient, db):
        """Обновление корзины"""
        from tests.factories import CategoryFactory, ProductFactory
        
        cat = CategoryFactory.create(db)
        prod = ProductFactory.create(db, category_id=cat.id)
        
        response = client.put(
            "/api/cart/update",
            json={"product_id": str(prod.id), "quantity": 5, "cart": {str(prod.id): 2}}
        )
        assert response.status_code == 200
    
    def test_remove_from_cart(self, client: TestClient, db):
        """Удаление из корзины"""
        from tests.factories import CategoryFactory, ProductFactory
        
        cat = CategoryFactory.create(db)
        prod = ProductFactory.create(db, category_id=cat.id)
        
        response = client.delete(f"/api/cart/remove/{prod.id}")
        assert response.status_code == 200


@pytest.mark.smoke
class TestHealth:
    """Базовые проверки здоровья приложения"""
    
    def test_root(self, client: TestClient):
        """Root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
    
    def test_health(self, client: TestClient):
        """Health check"""
        response = client.get("/health")
        assert response.status_code == 200
    
    def test_docs(self, client: TestClient):
        """Swagger доступен"""
        response = client.get("/api/docs")
        assert response.status_code == 200
    
    def test_redoc(self, client: TestClient):
        """ReDoc доступен"""
        response = client.get("/api/redoc")
        assert response.status_code == 200
