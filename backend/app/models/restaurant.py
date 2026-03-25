from sqlalchemy import Column, String, Integer
from app.database import Base

class Restaurant(Base):
    __tablename__ = "restaurants"

    # ID is an integer from 1 to 100
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False) 
    category = Column(String, nullable=True)