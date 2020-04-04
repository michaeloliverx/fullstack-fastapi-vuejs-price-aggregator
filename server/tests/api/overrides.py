"""
Endpoint dependency overrides are defined here.
"""

from tests import common


def override_get_db():
    """
    Override for get_db route dependency.
    Provides the scoped session used in testing.
    """
    db = common.ScopedSession()

    try:
        yield db
    finally:
        db.close()
