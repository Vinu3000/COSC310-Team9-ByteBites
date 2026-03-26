import pytest
from unittest.mock import MagicMock
from app.services.order_service import OrderService
from app.models.enums import OrderStatus

def test_invalid_status_transition():
    # Setup mocks for dependencies
    service = OrderService(MagicMock(), MagicMock(), MagicMock(), MagicMock())
    
    # Mock an existing order in Pending status
    service.order_repository.get_by_id.return_value = {"status": OrderStatus.PENDING}
    
    # Verify that jumping from Pending to Completed fails
    with pytest.raises(ValueError, match="Invalid transition"):
        service.update_order_status("123", OrderStatus.COMPLETED)

def test_order_not_found_exception():
    # Setup service with mocks
    service = OrderService(MagicMock(), MagicMock(), MagicMock(), MagicMock())
    
    # Mock repository returning None
    service.order_repository.get_by_id.return_value = None
    
    # Check if it raises the correct error message
    with pytest.raises(ValueError, match="not found"):
        service.update_order_status("999", OrderStatus.PREPARING)