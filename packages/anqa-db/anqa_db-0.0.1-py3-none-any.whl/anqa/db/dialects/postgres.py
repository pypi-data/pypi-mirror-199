from sqlalchemy.dialects.postgresql import insert

from ..repository import SQLAlchemyModelRepository


class PostgresModelRepository(SQLAlchemyModelRepository, abstract=True):
    _insert = staticmethod(insert)
    supports_returning = True
    supports_on_conflict = True
