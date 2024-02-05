from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "Users"

    uid = Column(Integer, primary_key=True)
    password = Column(String, nullable=False)
    created_dt = Column(DateTime, nullable=False)
    image_id = Column(String, nullable=False)
    name = Column(String, nullable=False)
