from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from config import settings
from alembic.config import Config
from alembic import command

engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def run_migrations():
    """Автоматичний запуск міграцій під час старту застосунку"""
    print("Running automatic DB migrations...")
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")
