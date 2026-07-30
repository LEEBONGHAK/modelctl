from sqlmodel import SQLModel
from sqlmodel import create_engine

_engine = None


def get_engine(db_path):

    global _engine

    if _engine is None:
        _engine = create_engine(f"sqlite:///{db_path}")

        SQLModel.metadata.create_all(_engine)

    return _engine
