from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Determine if the database URL targets SQLite
is_sqlite = settings.DATABASE_URL.startswith("sqlite")

# Add thread pooling check exclusions if running on SQLite
connect_args = {"check_same_thread": False} if is_sqlite else {}

# Initialize database engine with configuration options
engine = create_engine(
    settings.DATABASE_URL,
    connect_args=connect_args,
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
