from sqlmodel import Session


class Repository:
    def __init__(self, engine):

        self.engine = engine

    def session(self):

        return Session(self.engine)
