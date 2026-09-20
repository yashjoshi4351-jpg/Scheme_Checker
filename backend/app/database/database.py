from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

try:
    from app.config.settings import settings
    DATABASE_URL = settings.DATABASE_URL
except (ImportError, AttributeError):
    DATABASE_URL = "sqlite:///./government_schemes.db"


# SQLite needs this option for FastAPI's request-based usage.
connect_args = {}

if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}


engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    future=True,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()


def get_db():
    """
    Provides a database session for FastAPI dependencies.
    """
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Creates all registered database tables.
    """
    # Import models before create_all so SQLAlchemy knows about them.
    from app.models.user import User
    from app.models.scheme import Scheme
    from app.models.rule import Rule
    from app.models.eligibility_result import EligibilityResult

    Base.metadata.create_all(bind=engine)


# Alias for backward/seeder compatibility
create_tables = init_db