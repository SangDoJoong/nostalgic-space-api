from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "Users"

    uid = Column(Integer, primary_key=True)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
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