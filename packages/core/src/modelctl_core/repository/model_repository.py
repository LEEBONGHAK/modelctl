from sqlmodel import Session
from sqlmodel import select
from sqlalchemy.dialects.sqlite import insert
from datetime import datetime

from modelctl_core.models.universal_model import UniversalModel


class ModelRepository:
    def __init__(self, engine):
        self.engine = engine

    def upsert_many(self, models: list[UniversalModel]):
        with Session(self.engine) as session:
            for model in models:
                stmt = insert(UniversalModel).values(**model.model_dump(exclude={"id"}))

                stmt = stmt.on_conflict_do_update(
                    index_elements=["model_id"],
                    set_={
                        "display_name": stmt.excluded.display_name,
                        "context_length": stmt.excluded.context_length,
                        "prompt_price": stmt.excluded.prompt_price,
                        "completion_price": stmt.excluded.completion_price,
                        "updated_at": datetime.utcnow(),
                    },
                )
                session.exec(stmt)

            session.commit()

    def search(self, keyword: str):
        with Session(self.engine) as session:
            stmt = select(UniversalModel).where(UniversalModel.model_id.contains(keyword))

            return session.exec(stmt).all()

    def favorite(self, model_id: str, enabled: bool = True):
        with Session(self.engine) as session:
            model = session.exec(
                select(UniversalModel).where(UniversalModel.model_id == model_id)
            ).one()

            model.favorite = enabled
            session.add(model)
            session.commit()

    def recent(
        self,
        limit: int = 20,
    ):

        with Session(self.engine) as session:
            stmt = select(UniversalModel).order_by(UniversalModel.last_used_at.desc()).limit(limit)

            return session.exec(stmt).all()

    def get(self):
        return ""

    def exists(self):
        return ""

    def mark_used(
        self,
        model_id: str,
    ):

        with Session(self.engine) as session:
            model = ""

            model.last_used_at = datetime.utcnow()

            session.add(model)

            session.commit()
