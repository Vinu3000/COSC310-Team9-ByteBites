from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from app.database import Base

class Restaurant(Base):
    __tablename__ = "restaurants"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False) 
    category = Column(String, nullable=True)
    
    # This tells SQLAlchemy to find all MenuItems linked to this ID
    menu = relationship("MenuItem", back_populates="restaurant", cascade="all, delete-orphan")