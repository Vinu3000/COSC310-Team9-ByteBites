import uuid
from types import SimpleNamespace
from typing import List, Dict, Any

def filter_restaurants(data: List[Any], q: str = None, category: str = None) -> List[Any]:
    # Convert dictionaries to objects for consistent attribute access
    objects = [
        SimpleNamespace(**item) if isinstance(item, dict) else item 
        for item in data
    ]
    
    results = objects
    
    # 1. Category Filtering
    if category:
        results = [
            r for r in results 
            if getattr(r, "cuisine_type", None) == category or getattr(r, "category", None) == category
        ]

    # 2. Enhanced Search Query (Restaurant Name, Title, OR Menu Items)
    if q:
        query_lower = q.lower()
        search_results = []
        for r in results:
            # Check Restaurant attributes
            name_match = query_lower in getattr(r, "name", "").lower()
            title_match = query_lower in getattr(r, "title", "").lower()
            
            # Check Menu Item attributes
            menu_items = getattr(r, "menu", [])
            menu_match = False
            if isinstance(menu_items, list):
                for item in menu_items:
                    # Handle if menu items are dicts or objects
                    item_name = item.get("name", "") if isinstance(item, dict) else getattr(item, "name", "")
                    if query_lower in item_name.lower():
                        menu_match = True
                        break
            
            if name_match or title_match or menu_match:
                search_results.append(r)
        results = search_results
    
    return results

def paginate_data(data: List[Any], page: int, size: int) -> tuple:
    total = len(data)
    start = (page - 1) * size
    end = start + size
    sliced = data[start:end]
    total_pages = (total + size - 1) // size if size > 0 else 0
    return sliced, total_pages

def map_to_restaurant_schema(items: List[Any]) -> List[Dict[str, Any]]:
    formatted = []
    for item in items:
        obj = SimpleNamespace(**item) if isinstance(item, dict) else item
        
        try:
            val = getattr(obj, "id", 0)
            fake_uuid = uuid.UUID(int=int(val))
        except (AttributeError, ValueError, TypeError):
            fake_uuid = uuid.uuid4()

        raw_menu = getattr(obj, "menu", [])
        # Ensure menu items are formatted as objects or preserved as dicts 
        # depending on your Pydantic schema requirements
        formatted_menu = [
            SimpleNamespace(**m) if isinstance(m, dict) else m 
            for m in raw_menu
        ] if isinstance(raw_menu, list) else []

        formatted.append({
            "id": fake_uuid,
            "name": getattr(obj, "name", getattr(obj, "title", "Unknown")),
            "title": getattr(obj, "title", getattr(obj, "name", "Unknown")),
            "location": getattr(obj, "location", "UBCO Campus"),
            "cuisine_type": getattr(obj, "cuisine_type", getattr(obj, "category", "N/A")),
            "category": getattr(obj, "category", getattr(obj, "cuisine_type", "N/A")),
            "rating": getattr(obj, "rating", 0.0),
            "menu": formatted_menu  
        })
    return formatted