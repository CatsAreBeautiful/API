from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from sqlmodel import Field, Session, SQLModel, create_engine, select

class Users(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Start App")
    SQLModel.metadata.create_all(engine)
    yield

app = FastAPI(lifespan=lifespan)

@app.post("/users/add/")
async def add_user(name: str):
    with Session(engine) as session:
        statement = select(Users).where(Users.name == name)
        # results = session.exec(statement)
        if session.exec(statement).first() is None:
            session.add(Users(name=name))
            session.commit()
            return {"message": f"User {name} sucessfully added!"}
        else:
            raise HTTPException(status_code=404, detail="User already exists!")

@app.delete("/users/del")
async def del_user(name: str):
    with Session(engine) as session:
        statement = select(Users).where(Users.name == name)
        # results = session.exec(statement)
        if session.exec(statement).first() is None:
            raise HTTPException(status_code=404, detail="User not exists!")
        else:
            user = session.query(Users).filter_by(name=name).one()
            session.delete(user)
            session.commit()
            return {"message": f"User {name} sucessfully deleted!"}