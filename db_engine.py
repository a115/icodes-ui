from sqlmodel import Session, create_engine
from icds.settings import settings

engine = create_engine(settings.DATABASE_URL)


def get_db_session():
    with Session(engine) as session:
        yield session
