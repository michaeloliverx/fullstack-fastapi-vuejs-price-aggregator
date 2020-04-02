from sqlalchemy import orm

from app.db.session import SessionLocal

ScopedSession = orm.scoped_session(SessionLocal)

# Password used for models
USER_PASSWORD = "VerySafePassword01!"


def override_get_db():
    """
    Override for get_db route dependency.
    Provides the scoped session used in testing.
    """
    db = ScopedSession()
    try:
        yield db
    finally:
        db.close()
