from sqlalchemy import orm

from app.db.session import SessionLocal

# Password used for models
USER_PASSWORD = "VerySafePassword01!"

# Provides a global reference to an existing session.
ScopedSession = orm.scoped_session(SessionLocal)
