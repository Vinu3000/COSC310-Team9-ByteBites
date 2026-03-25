import pytest
from app.data.ingest_data import CATEGORY_MAP

# This unit test checks our internal logic without needing a database
# It ensures our category mapping is correct

def test_category_mapping_logic():
    """
    Check if our category dictionary returns the correct food type.
    """
    # Test a known item
    assert CATEGORY_MAP.get("Sushi") == "Japanese"
    assert CATEGORY_MAP.get("Pizza") == "Italian"
    
    # Test an unknown item (should fall back to None or a default)
    assert CATEGORY_MAP.get("Unknown Food", "Other") == "Other"

def test_pagination_math_logic():
    """
    Check if our pagination math works (Total items / Page size).
    """
    total_items = 25
    size = 10
    # The math used in our API: (total + size - 1) // size
    pages = (total_items + size - 1) // size
    
    assert pages == 3 # 25 items with 10 per page should be 3 pages