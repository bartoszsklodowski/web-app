from sqlalchemy import Column, Integer, String

from database import Base


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True)
    date = Column(String)
    date_added = Column(String, default=True)
