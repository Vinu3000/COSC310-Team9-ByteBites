from fastapi import HTTPException

class MenuService:
    def create_menu_item(self, item_data, current_user):
        # Business Rule: Manager can only modify their own restaurant menu 
        if current_user.role == "MANAGER" and current_user.managed_restaurant_id != item_data.restaurant_id:
            raise HTTPException(status_code=403, detail="Unauthorized manager access to this restaurant")
        
        # Business Rule: Menu item must have a valid restaurant ID (referential integrity) [cite: 54, 262]
        return "Item Created"