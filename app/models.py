from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry

from database import Base


class User(Base):
    __tablename__ = "Users"

    uid = Column(Integer, primary_key=True)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    image_id = Column(String, nullable=False)
    username = Column(String, nullable=False)

class Image(Base):
    __tablename__ = "Images"

    image_id = Column(Integer, primary_key=True)
    image_address = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)


class UserImage(Base):
    __tablename__ = "Users_Images"
    id =Column(Integer, primary_key=True)
    user_id =Column(Integer, primary_key=False)
    image_id =Column(Integer, primary_key=False)

class ContentImage(Base):
    __tablename__ = "Contents_Images"
    id =Column(Integer, primary_key=True)
    content_id =Column(Integer, primary_key=False)
    image_id =Column(Integer, primary_key=False)
    
class Map(Base):
    __tablename__ = "Maps"
    map_id = Column(Integer, primary_key=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    location = Column(Geometry('POINT'), nullable=False)
    uid = Column(Integer, nullable=False)
    content_id = Column(Integer, nullable=False)
