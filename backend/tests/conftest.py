import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from pathlib import Path
import sys

# Путь к приложению
sys.path.insert(0, str(Path(__file__).parent.parent))

# ✅ ЯВНО ИМПОРТИРУЕМ APP
from app.main import app
from app.database import Base, get_db

# ==================== КОНФИГУРАЦИЯ БД ====================
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Включаем foreign keys для SQLite
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_conn, connection_record):
    cursor = dbapi_conn.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Создаём таблицы один раз при загрузке конфига
Base.metadata.create_all(bind=engine)

# ==================== ФИКСТУРЫ ====================

@pytest.fixture(scope="function")
def db():
    """
    Фикстура БД - каждый тест работает в отдельной транзакции.
    Транзакция откатывается после теста = БД остаётся чистой.
    """
    # Открываем соединение
    connection = engine.connect()
    
    # Начинаем транзакцию
    transaction = connection.begin()
    
    # Создаём сессию для этой транзакции
    session = TestingSessionLocal(bind=connection)
    
    # Переопределяем get_db для приложения
    def override_get_db():
        yield session
    
    app.dependency_overrides[get_db] = override_get_db
    
    # Возвращаем сессию тесту
    yield session
    
    # Откатываем транзакцию (удаляет все изменения)
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def client(db):
    """
    Фикстура TestClient - подключена к тестовой БД.
    ✅ КРИТИЧЕСКИ: явно обернуть app в TestClient!
    """
    # ✅ ЯВНО оборачиваем app в TestClient
    test_client = TestClient(app)
    return test_client
