from pydantic import BaseModel


class EventBase(BaseModel):
    date: str
    event: str


class EventCreate(EventBase):
    pass


class Event(EventBase):
    id: int
    date_added: str

    class Config:
        orm_mode = True
