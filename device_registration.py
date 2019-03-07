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
    house_id = Column(Integer)
    status = Column(String)
    image = Column(String)

    def __init__(self, name, house_id, status, image):

        self.name = name
        self.house_id = house_id
        self.status = status
        self.image = image

Base.metadata.create_all(engine)
