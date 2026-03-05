from uuid import UUID, uuid4

class MenuRepository:
    def __init__(self):
        self._menu_items = []

    def create(self, item_data) -> dict:
        """Store a new menu item with a unique ID[cite: 256]."""
        new_item = item_data.dict()
        new_item["id"] = uuid4()
        self._menu_items.append(new_item)
        return new_item

    def get_by_id(self, item_id: UUID):
        return next((i for i in self._menu_items if i["id"] == item_id), None)