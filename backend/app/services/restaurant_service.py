import uuid
from typing import List, Dict, Any

def filter_restaurants(data: List[Any], q: str = None, category: str = None) -> List[Any]:
    """
    This function looks through the list and keeps only the ones 
    that match the name or the food type.
    """
    results = data
    # If the user typed a search word, we check if it is in the title
    if q:
        results = [r for r in results if q.lower() in r.title.lower()]
    
    # If the user picked a category, we filter by that too
    if category:
        results = [r for r in results if r.category == category]
    
    return results

def paginate_data(data: List[Any], page: int, size: int) -> tuple:
    """
    This function cuts the big list into a small piece 
    based on the page number and how many items we want to see.
    """
    total = len(data)
    # Find where the page starts and ends
    start = (page - 1) * size
    end = start + size
    sliced = data[start:end]
    
    # Math to figure out how many total pages we need
    if size > 0:
        total_pages = (total + size - 1) // size
    else:
        total_pages = 0
        
    return sliced, total_pages

def map_to_restaurant_schema(items: List[Any]) -> List[Dict[str, Any]]:
    """
    This function changes the raw data into the format 
    that the restaurant schema expects.
    """
    formatted = []
    for item in items:
        # We turn the simple ID number into a real UUID object
        fake_uuid = uuid.UUID(int=int(item.id)) 
        
        # We build the dictionary for the API response
        formatted.append({
            "id": fake_uuid,
            "name": item.title,
            "location": "UBCO Campus",
            "category": item.category
        })
    return formatted