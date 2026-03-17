from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import Config

# Motor de SQLAlchemy usando la URI de Config
engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)

# Sesión para uso manual (SessionLocal())
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# Base para modelos ORM si se migran a SQLAlchemy
Base = declarative_base()

def init_db():
    """Crear tablas definidas en los modelos ORM (si existen)."""
    Base.metadata.create_all(bind=engine)
