from sqlalchemy import create_engine
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

engine = create_engine('sqlite:///devices.db', echo=True)
Base = declarative_base()

class Device(Base):

    __tablename__ = "devices"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    house = Column(String)
    status = Column(String)

    def __init__(self, name, house, status):

        self.name = name
        self.house = house
        self.status = status

Base.metadata.create_all(engine)
