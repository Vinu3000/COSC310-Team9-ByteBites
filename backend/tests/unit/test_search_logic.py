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

# --- Edge Case Tests ---

def test_pagination_out_of_bounds():
    """
    Check if it returns an empty list when the page number is too high.
    """
    fake_data = list(range(5))  # Only 5 items
    size = 10
    
    # Requesting page 2 should return no items, but NOT crash
    sliced, total_pages = paginate_data(fake_data, page=2, size=size)
    
    assert len(sliced) == 0
    assert total_pages == 1

def test_filter_no_match():
    """
    Check if it returns an empty list when the search word doesn't exist.
    """
    class MockItem:
        def __init__(self, title, category):
            self.title = title
            self.category = category

    items = [MockItem("Pizza", "Italian")]
    
    # Searching for something that isn't there
    results = filter_restaurants(items, q="Sushi")
    
    assert len(results) == 0

def test_filter_case_insensitivity_and_partial_match():
    """
    Check if 'piz' can find 'Pizza Place'. Users often type partial words.
    """
    class MockItem:
        def __init__(self, title, category):
            self.title = title
            self.category = category

    items = [MockItem("Pizza Place", "Italian")]
    
    # Partial match and mixed case
    results = filter_restaurants(items, q="pIz")
    
    assert len(results) == 1
    assert "Pizza" in results[0].title

def test_empty_data_handling():
    """
    Check if the code handles an empty database without crashing.
    """
    empty_list = []
    
    sliced, total_pages = paginate_data(empty_list, page=1, size=10)
    
    assert len(sliced) == 0
    assert total_pages == 0
