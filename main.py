from fastapi import FastAPI, Response, status, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
import crud
import models
import schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def task_1():
    return {"start": "1970-01-01"}


@app.get("/method")
def task_2():
    return {"method": "GET"}


@app.post("/method", status_code=201)
def task_2():
    return {"method": "POST"}


@app.delete("/method")
def task_2():
    return {"method": "DELETE"}


@app.put("/method")
def task_2():
    return {"method": "PUT"}


@app.options("/method")
def task_2():
    return {"method": "OPTIONS"}


@app.get("/day")
def task_3(response: Response, name: str | None = None, number: int | None = None):
    days = {1: "monday", 2: "tuesday", 3: "wednesday", 4: "thursday", 5: "friday", 6: "saturday", 7: "sunday"}
    response.status_code = status.HTTP_400_BAD_REQUEST
    if number in days:
        if days.get(number) == name:
            response.status_code = status.HTTP_200_OK
            return response.status_code
    return response.status_code


@app.put("/events", response_model=schemas.Event)
def task_4(event: schemas.EventCreate, db: Session = Depends(get_db)):
    return crud.create_event(db=db, event=event)


@app.get("/events", response_model=list[schemas.Event])
def task_4(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    events = crud.get_events(db, skip=skip, limit=limit)
    return events


@app.get("/events/{date}")
def task_5(date: str, db: Session = Depends(get_db)):
    events = crud.get_event_by_date(db, event_date=date)
    return list(events)

