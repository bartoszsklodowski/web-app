import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:DaftAcademy@127.0.0.1:5555"
SQLALCHEMY_DATABASE_URL = "postgresql://xsjljnrcbrrfdu:19e5ddeb78a4dbb7c9d077cca13d69ea106c0b6832f552d1b5dd10ca47b99322@ec2-99-80-170-190.eu-west-1.compute.amazonaws.com:5432/dab1htb6r28ekk"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


