from datetime import UTC, datetime

from sqlmodel import Session
from sqlmodel import select

from modelctl_core.models.universal_model import UniversalModel


class ModelRepository:
    def __init__(
        self,
        engine,
    ):

        self.engine = engine

    def save_many(
        self,
        models: list[UniversalModel],
    ):

        with Session(self.engine) as session:
            for model in models:
                existing = session.exec(
                    select(UniversalModel).where(UniversalModel.model_id == model.model_id)
                ).first()

                if existing:
                    existing.name = model.name

                    existing.context_length = model.context_length

                    existing.updated_at = datetime.now(UTC)

                else:
                    session.add(model)

            session.commit()

    def list(
        self,
    ):

        with Session(self.engine) as session:
            return session.exec(
                select(UniversalModel).order_by(UniversalModel.provider, UniversalModel.model_id)
            ).all()

    def search(
        self,
        keyword: str,
    ):

        with Session(self.engine) as session:
            return session.exec(
                select(UniversalModel).where(UniversalModel.model_id.contains(keyword))
            ).all()

    def favorite(
        self,
        model_id: str,
        value: bool,
    ):

        with Session(self.engine) as session:
            model = session.exec(
                select(UniversalModel).where(UniversalModel.model_id == model_id)
            ).first()

            if model:
                model.favorite = value

                session.add(model)

                session.commit()

    def favorites(self):

        with Session(self.engine) as session:
            return session.exec(select(UniversalModel).where(UniversalModel.favorite == True)).all()
