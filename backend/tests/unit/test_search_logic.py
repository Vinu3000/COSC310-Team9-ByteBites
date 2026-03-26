import pytest
from app.data.ingest_data import CATEGORY_MAP
from app.services.restaurant_service import filter_restaurants, paginate_data


def test_category_mapping_logic():
    """ Check if our category dictionary returns the correct food type. """
    assert CATEGORY_MAP.get("Sushi") == "Japanese"
    assert CATEGORY_MAP.get("Pizza") == "Italian"

# --- Refactored Tests ---

def test_pagination_math_logic():
    """
    no longer write the math inside the test. 
    call the actual function to see if it works
    """
    # Create a list with 25 items
    fake_data = list(range(25))
    size = 10
    
    # Call the real function from our service
    _, pages = paginate_data(fake_data, page=1, size=size)
    
    # It should still be 3
    assert pages == 3

def test_filter_logic_unit():
    """
    Check if our search filter actually finds the right words.
    """
    # A simple class to act like a data object
    class MockItem:
        def __init__(self, title, category):
            self.title = title
            self.category = category

    items = [MockItem("Burger Joint", "Fast Food"), MockItem("Pizza Place", "Italian")]
    
    # Test if it finds 'burger'
    results = filter_restaurants(items, q="BURGER")
    
    assert len(results) == 1
    assert results[0].title == "Burger Joint"