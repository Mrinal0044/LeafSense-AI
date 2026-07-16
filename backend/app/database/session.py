from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Initialize database engine with configuration options for PostgreSQL
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True  # Detect stale/disconnected connections in Postgres
)

# Configure Session local factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def get_db():
    """
    Request database session dependency injection container.
    Closes database session when request thread concludes.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
