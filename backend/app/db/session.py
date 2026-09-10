from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

connect_args = {}
db_url = settings.sqlalchemy_database_url
if db_url.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(
    db_url,
    connect_args=connect_args,
    echo=False
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """
    Generador de sesión SQLAlchemy para Dependency Injection en FastAPI.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
