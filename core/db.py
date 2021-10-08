import contextlib
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
engine = create_engine('sqlite:///C:\\Users\\User\\Desktop\\test.db', echo=True)
@contextlib.contextmanager
def create_session(commit = True):
    with Session(engine) as session:
        yield session
        if commit:
            session.commit()