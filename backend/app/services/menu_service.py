from fastapi import HTTPException, status
from uuid import UUID

class MenuService:
    def __init__(self, menu_repo, restaurant_repo):
        self.menu_repo = menu_repo
        self.restaurant_repo = restaurant_repo

    def add_menu_item(self, item_data, current_user):
        
        restaurant = self.restaurant_repo.get_by_id(item_data.restaurant_id)
        if not restaurant:
            raise HTTPException(status_code=404, detail="Restaurant not found")

        if current_user.role != "ADMIN" and current_user.managed_restaurant_id != item_data.restaurant_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="Unauthorized: You can only manage your own restaurant's menu"
            )

        return self.menu_repo.create(item_data)