from pydantic import BaseModel


class EventBase(BaseModel):
    name: str
    date: str



class EventCreate(BaseModel):
    date: str
    event: str


class Event(EventBase):
    id: int
    date_added: str

    class Config:
        orm_mode = True
