from sqlalchemy.orm import Session
from datetime import date

import models
import schemas


def get_event_by_date(db: Session, event_date: str):
    return db.query(models.Event).filter(models.Event.date == event_date)


def get_events(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Event).offset(skip).limit(limit).all()


def create_event(db: Session, event: schemas.EventCreate):
    event_date = event.date
    event_name = event.event
    date_added = date.today().strftime("%Y-%m-%d")
    db_event = models.Event(event=event_name, date=event_date, date_added=date_added)
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event
