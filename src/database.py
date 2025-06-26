import os
from sqlmodel import create_engine, Session


user = os.getenv("dbuser")
password = os.getenv("dbpass")

DATABASE_URL = f"postgresql://{user}:{password}@postgres:5432/users"
engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    return Session(engine)

