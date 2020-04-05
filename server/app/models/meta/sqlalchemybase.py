from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import EmailType, generic_repr


@generic_repr
class SQLAlchemyBase:
    """
    SQLAlchemyBase class.
    """

    __abstract__ = True

    # https://gist.githubusercontent.com/mjhea0/9b9c400a2bc58e6c90e5f77eeb739d6b/raw/2ca3e8c696011b500cf2864cd4a8f125112f4251/base_mixin.py
    # _repr_hide = ["created_at", "updated_at"]
    #
    # def __repr__(self):  # pragma: no cover
    #     values = ", ".join(
    #         "%s=%r" % (n, getattr(self, n))
    #         for n in self.__table__.c.keys()
    #         if n not in self._repr_hide
    #     )
    #     return "%s(%s)" % (self.__class__.__name__, values)


SQLAlchemyBase = declarative_base(cls=SQLAlchemyBase)
