from sqlalchemy import create_engine
from sqlalchemy.orm import  sessionmaker, declarative_base
from src.config.settings import Settings

# Motor para conexión con la BD
engine = create_engine(
    Settings.DATABASE_URL
)

# Patrón Fábrica para crear sesiones
SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine
)

Base = declarative_base()
