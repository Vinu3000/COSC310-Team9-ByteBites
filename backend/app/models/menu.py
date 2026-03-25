from sqlalchemy import Column, String, Float, ForeignKey, Integer
from app.database import Base

class MenuItem(Base):
    __tablename__ = "menu_items"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    
    # Menu item must have valid restaurant ID
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"), nullable=False)