from sqlalchemy import create_engine
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

engine = create_engine('sqlite:///contractors.db', echo=True)
Base = declarative_base()

class Contractor(Base):

    __tablename__ = "contractors"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    password = Column(String, unique=True)

    def __init__(self, name, email, username, password):

        self.name = name
        self.email = email
        self.username = username
        self.password = password

Base.metadata.create_all(engine)
