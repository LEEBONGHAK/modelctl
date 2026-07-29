from sqlmodel import SQLModel, create_engine

from modelctl.core.paths import database_file


engine = create_engine(
    f"sqlite:///{database_file()}",
    echo=False
)



def init_database():

    SQLModel.metadata.create_all(
        engine
    )
