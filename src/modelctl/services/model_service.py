from sqlmodel import Session, select

from modelctl.core.database import engine
from modelctl.models.model import Model



def save_models(
    provider_name,
    models
):

    with Session(engine) as session:


        for item in models:

            model = Model(
                provider=provider_name,
                model_id=item["id"],
                name=item.get("name"),
                context_length=item.get(
                    "context_length"
                )
            )


            session.add(model)


        session.commit()



def get_models():

    with Session(engine) as session:

        statement = select(Model)

        return session.exec(
            statement
        ).all()
