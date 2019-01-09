from sqlalchemy import create_engine
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

engine = create_engine('sqlite:///houses.db', echo=True)
Base = declarative_base()

class House(Base):

    __tablename__ = "houses"

    id = Column(Integer, primary_key=True)
    owner = Column(String)
    name = Column(String)
    location = Column(String)

    def __init__(self, owner, name, location):

        self.owner = owner
        self.name = name
        self.location = location

Base.metadata.create_all(engine)
