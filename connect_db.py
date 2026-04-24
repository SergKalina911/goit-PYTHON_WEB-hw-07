"""Код який підключає  проєкт до PostgreSQL через SQLAlchemy.
Пояснення:
- DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME — параметри для підключення.
- DATABASE_URL — стандартний формат для SQLAlchemy:
    
    postgresql://user:password@host:port/dbname

- engine — об’єкт для роботи з БД.
- session — використовується у всіх запитах (my_select.py, seed.py, main.py)."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Параметри підключення до PostgreSQL
DB_USER = "postgres"
DB_PASSWORD = "mysecretpassword"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "school"

# Формуємо URL для SQLAlchemy
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Створюємо engine
engine = create_engine(DATABASE_URL, echo=False)

# Створюємо сесію
Session = sessionmaker(bind=engine)
session = Session()
