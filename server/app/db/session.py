from sqlalchemy import create_engine, orm

from app.settings import settings

engine = create_engine(settings.POSTGRES_URL, pool_pre_ping=True)
SessionLocal = orm.sessionmaker(bind=engine)


def get_db():
    """Endpoint dependency for getting db session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
