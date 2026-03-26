from fastapi import HTTPException, status
from app.models.menu import MenuItem

class MenuService:
    def __init__(self, db):
        self.db = db

    def get_restaurants(self, page: int = 1, size: int = 10):
        # Business Rule: Pagination required
        offset = (page - 1) * size
        return self.db.query(Restaurant).offset(offset).limit(size).all()

    def update_menu_item(self, item_id: int, user: dict, update_data: dict):
        item = self.db.query(MenuItem).filter(MenuItem.id == item_id).first()
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        
        # Business Rule: Manager can only modify own restaurant menu
        if user["role"] == "MANAGER" and item.restaurant_id != user.get("managed_restaurant_id"):
            raise HTTPException(status_code=403, detail="Unauthorized manager")
        
        for key, value in update_data.items():
            setattr(item, key, value)
        self.db.commit()
        return item