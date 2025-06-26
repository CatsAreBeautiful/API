from fastapi import FastAPI, HTTPException
from sqlmodel import SQLModel, Session, select
import tldextract

from models import Users
from database import engine


app = FastAPI()

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

@app.post("/create")
def create(domain: str, user: str):
    with Session(engine) as session:
        statement = select(Users).where(Users.domain == domain)
        if session.exec(statement).first():
            raise HTTPException(status_code=400, detail="Domain already exists")

        session.add(Users(user=user, domain=domain))
        session.commit()

    return {"message": f"User {user} and domain {domain} created successfully"}

@app.get("/check")
def check_domain(domain: str):
    extracted_domain = tldextract.extract(domain).top_domain_under_public_suffix


    with Session(engine) as session:
        statement = select(Users).where(Users.domain == extracted_domain)
        results = session.exec(statement).all()

        if not results:
            raise HTTPException(status_code=404, detail="Domain not found in database")

        user = results[0]

    return {
        "domain": domain,
        "user": user
    }
