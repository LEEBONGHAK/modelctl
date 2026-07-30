from sqlmodel import Session
from sqlmodel import select

from modelctl_core.models.universal_model import UniversalModel


class ModelRepository:

    def __init__(self, engine):
        self.engine = engine

    def save_many(self, models: list[UniversalModel]):

        with Session(self.engine) as session:

            for model in models:
                session.merge(model)

            session.commit()

    def list(self):

        with Session(self.engine) as session:

            return session.exec(
                select(UniversalModel)
            ).all()

    def delete_all(self):

        with Session(self.engine) as session:

            rows = session.exec(
                select(UniversalModel)
            ).all()

            for row in rows:
                session.delete(row)

            session.commit()