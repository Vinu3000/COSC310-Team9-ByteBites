from app.models.menu import MenuItem

class MenuRepository:
    def __init__(self, db):
        self.db = db

    def create(self, data_dict):
        item = MenuItem(**data_dict)
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item