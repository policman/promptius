# добавление корня проекта в PYTHONPATH
import os
import sys
from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
#load_dotenv('.env')
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))


print("✅✅✅ Loaded SYNC_DATABASE_URL:", os.getenv("SYNC_DATABASE_URL"))


from logging.config import fileConfig
from sqlalchemy import create_engine, pool
from alembic import context

from app.core.database import Base
from app.models import user  # все модели, чтобы Alembic их "видел"

# получаем переменные
#DATABASE_URL: str = os.getenv("DATABASE_URL") or ""
DATABASE_URL = os.getenv("SYNC_DATABASE_URL") or ""
print(f"✅ Using DATABASE_URL: {DATABASE_URL}")


# Alembic Config
config = context.config

# Логирование Alembic
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Метаданные всех моделей
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Запуск миграций в offline-режиме (без подключения к БД)."""
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Запуск миграций в online-режиме (c подключением к БД)."""
    connectable = create_engine(
        DATABASE_URL,
        poolclass=pool.NullPool,
        future=True,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,  # чтобы Alembic отслеживал изменения типов
        )

        with context.begin_transaction():
            context.run_migrations()


# Запускаем нужный режим
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
