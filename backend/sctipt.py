import sqlite3
import uuid
from datetime import datetime

db_path = 'shop.db'

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute('DROP TABLE IF EXISTS products_new')

# Создаем новую таблицу по вашей модели
cursor.execute('''
CREATE TABLE products_new (
    id TEXT PRIMARY KEY NOT NULL,
    name TEXT UNIQUE NOT NULL,
    description TEXT,
    price REAL NOT NULL,
    category_id INTEGER NOT NULL,
    image_url TEXT,
    created_at TEXT DEFAULT (datetime('now'))
)
''')

# Выборка всех данных из старой таблицы
cursor.execute('SELECT id, name, description, price, category_id, image_url, created_at FROM products')
rows = cursor.fetchall()

for row in rows:
    old_id, name, description, price, category_id, image_url, created_at = row
    new_id = str(uuid.uuid4())  # генерируем новый UUID
    # Если created_at пустой, ставим текущую дату в стандартном формате ISO
    created_at_val = created_at if created_at else datetime.utcnow().isoformat()
    cursor.execute('''
        INSERT INTO products_new (id, name, description, price, category_id, image_url, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (new_id, name, description, price, category_id, image_url, created_at_val))

# Удаляем старую таблицу
cursor.execute('DROP TABLE products')

# Переименовываем новую таблицу в products
cursor.execute('ALTER TABLE products_new RENAME TO products')

conn.commit()
conn.close()

print("Миграция базы данных завершена успешно.")
