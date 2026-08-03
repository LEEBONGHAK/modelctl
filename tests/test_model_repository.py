from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel, create_engine

from modelctl_core.models.universal_model import UniversalModel
from modelctl_core.repository.model_repository import ModelRepository


def create_repository() -> ModelRepository:
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    return ModelRepository(engine)


def test_repository_lists_and_finds_models_by_provider():
    repository = create_repository()
    repository.save_many(
        [
            UniversalModel(
                provider="openrouter",
                model_id="anthropic/claude-sonnet-4",
                name="Claude Sonnet 4",
            ),
            UniversalModel(
                provider="other",
                model_id="other/model",
                name="Other Model",
            ),
        ]
    )

    models = repository.list_by_provider("openrouter")

    assert [model.model_id for model in models] == ["anthropic/claude-sonnet-4"]
    assert (
        repository.get_by_provider("openrouter", "anthropic/claude-sonnet-4")
        is not None
    )
    assert repository.get_by_provider("openrouter", "missing/model") is None
