from sqlalchemy import Column, Integer, Float, DateTime, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine
from sqlalchemy.sql import func

Base = declarative_base()


class Weather(Base):
    __tablename__ = 'weather'

    id = Column(Integer, primary_key=True)
    location_id = Column(Integer, ForeignKey('location.id'))
    dtm = Column(DateTime(timezone=True), server_default=func.now())
    temperature = Column(Float(asdecimal=True))
    pressure = Column(Float(asdecimal=True))

    location = relationship("Location")


class Location(Base):
    __tablename__ = 'location'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    altitude = Column(Integer)


engine = create_engine('sqlite:///meteo.db')  # echo=True
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
