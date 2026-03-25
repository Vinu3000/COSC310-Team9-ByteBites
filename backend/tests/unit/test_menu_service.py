from unittest.mock import MagicMock
import pytest
from app.services.menu_service import MenuService
from fastapi import HTTPException

def test_manager_cannot_modify_other_restaurant():
    # Setup: Mock the DB and the existing item
    mock_db = MagicMock()
    mock_item = MagicMock()
    mock_item.restaurant_id = 1  # Item belongs to Restaurant 1
    
    service = MenuService(mock_db)
    
    # User is a manager of Restaurant 2
    user = {"role": "MANAGER", "managed_restaurant_id": 2}
    
    # Action & Assert: Should raise 403
    with pytest.raises(HTTPException) as exc:
        service.update_menu_item(item_id=101, user=user, update_data={"price": 10.0})
    
    assert exc.value.status_code == 403
    assert "Unauthorized manager" in exc.value.detail