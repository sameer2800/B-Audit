from sqlalchemy import create_engine
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

engine = create_engine('sqlite:///services.db', echo=True)
Base = declarative_base()

class Service(Base):

    __tablename__ = "services"

    id = Column(Integer, primary_key=True)
    device_id = Column(Integer)
    contractor = Column(String)
    type = Column(String)
    cost = Column(Integer)
    status = Column(String)

    def __init__(self, device_id, contractor, type, cost, status):

        self.device_id = device_id
        self.contractor = contractor
        self.type = type
        self.cost = cost
        self.status = status

Base.metadata.create_all(engine)
