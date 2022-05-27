import datetime
import secrets
from fastapi import FastAPI, Response, status, Depends, HTTPException, Query, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from sqlalchemy.orm import Session
import crud
import models
import schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
security = HTTPBasic()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def validate(date_text):
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
    except ValueError:
        raise ValueError("Incorrect data format, should be YYYY-MM-DD")


@app.get("/")
def task_1_1():
    return {"start": "1970-01-01"}


@app.get("/method")
def task_1_2():
    return {"method": "GET"}


@app.post("/method", status_code=201)
def task_1_2():
    return {"method": "POST"}


@app.delete("/method")
def task_1_2():
    return {"method": "DELETE"}


@app.put("/method")
def task_1_2():
    return {"method": "PUT"}


@app.options("/method")
def task_1_2():
    return {"method": "OPTIONS"}


@app.get("/day")
def task_1_3(response: Response, name: str | None = None, number: int | None = None):
    days = {1: "monday", 2: "tuesday", 3: "wednesday", 4: "thursday", 5: "friday", 6: "saturday", 7: "sunday"}
    response.status_code = status.HTTP_400_BAD_REQUEST
    if number in days:
        if days.get(number) == name:
            response.status_code = status.HTTP_200_OK
            return response.status_code
    return response.status_code


@app.put("/events", response_model=schemas.Event)
def task_1_4(event: schemas.EventCreate, db: Session = Depends(get_db)):
    return crud.create_event(db=db, event=event)


@app.get("/events", response_model=list[schemas.Event])
def task_1_4(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    events = crud.get_events(db, skip=skip, limit=limit)
    return events


@app.get("/events/{date}")
def task_1_5(response: Response, date: str, db: Session = Depends(get_db)):
    try:
        datetime.datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return response.status_code
    events = crud.get_event_by_date(db, event_date=date)
    events_list = list(events)
    if events_list:
        return events_list
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return response.status_code


# ZADANIA CZEŚĆ 3

@app.get("/start", response_class=HTMLResponse)
def task_3_1():
    return """
        <h1>The unix epoch started at 1970-01-01</h1>
        """


from datetime import date


@app.post("/check", response_class=HTMLResponse)
def task_3_2(credentials: HTTPBasicCredentials = Depends(security)):
    try:
        datetime.datetime.strptime(credentials.password, '%Y-%m-%d')
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect date format",
            headers={"WWW-Authenticate": "Basic"},
        )
    date_of_birth = date.fromisoformat(credentials.password)
    today = date.today()
    age = today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
    if (age < 16):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are under 16",
            headers={"WWW-Authenticate": "Basic"},
        )
    return f"""<h1>Welcome {credentials.username}! You are {age}</h1>"""


import json


# uvicorn main:app --reload
@app.get("/info")
def task_3_3(request: Request, format: str | None = None):
    header = request.headers.get('User-Agent')
    if format == "json":
        data = {"user_agent": f"{header}"}
        return Response(content=json.dumps(data), media_type="application/json")

    elif format == "html":
        data = f"""<input type="text" id=user-agent name=agent value="{header}">"""
        return Response(content=data, media_type="application/html")
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Format param not json/html or param empty",
        )


list_of_strings = []


@app.get("/save/{string}")
@app.put("/save/{string}")
@app.delete("/save/{string}")
def task_3_4(request: Request, string: str | None = None):
    method = request.method
    if method == "GET":
        if string in list_of_strings:
            return RedirectResponse("/info", headers={"Location": "/info"}, status_code=301)
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="String not found",
            )
    elif method == "PUT":
        list_of_strings.append(string)
        return Response(status_code=200)
    elif method == "DELETE":
        if string in list_of_strings:
            list_of_strings.remove(string)
            return Response(status_code=200)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Method not allowed",
        )
