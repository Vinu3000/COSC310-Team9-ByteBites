# backend/app/api/v1/shared_data.py

# ==========================================
# User Identity & Roles
# ==========================================
mock_users_db = {
    "admin@bytebites.com": {"id": 1, "email": "admin@bytebites.com", "role": "admin", "name": "Claire Admin"},
    "user@gmail.com": {"id": 2, "email": "user@gmail.com", "role": "user", "name": "Regular Joe"}
}

# ==========================================
# Restaurants & Menus
# ==========================================
mock_restaurants_db = [
    {
        "id": 1, 
        "name": "Pizza Planet", 
        "cuisine_type": "Italian", 
        "rating": 4.8,
        "menu": [
            {"id": 101, "name": "Margherita Pizza", "price": 15.0, "category": "Main"},
            {"id": 102, "name": "Pepperoni Pizza", "price": 18.0, "category": "Main"},
            {"id": 103, "name": "Garlic Bread", "price": 6.5, "category": "Side"}
        ]
    },
    {
        "id": 2, 
        "name": "Burger Queen", 
        "cuisine_type": "American", 
        "rating": 4.5,
        "menu": [
            {"id": 201, "name": "Royal Cheese Burger", "price": 12.0, "category": "Main"},
            {"id": 202, "name": "Curly Fries", "price": 4.0, "category": "Side"},
            {"id": 203, "name": "Vanilla Shake", "price": 5.0, "category": "Drink"}
        ]
    }
]


mock_orders_db = {
    1: {
        "id": 1,
        "restaurant_name": "Pizza Planet",
        "items": [
            {"name": "Margherita Pizza", "price": 15.0},
            {"name": "Garlic Bread", "price": 6.5}
        ],
        "subtotal": 21.5,
        "delivery_fee": 5.0,
        "tax": 2.15,
        "total_price": 28.65,
        "status": "Preparing",        # Feature 5: Delivery Status
        "payment_status": "Success",   # Feature 7: Payment Status
        "refund_status": "None",       # For Admin: Refunds page
        "discount_applied": 0.0,
        "created_at": "2024-03-20 18:30:00"
    },
    2: {
        "id": 2,
        "restaurant_name": "Burger Queen",
        "items": [
            {"name": "Royal Cheese Burger", "price": 12.0}
        ],
        "subtotal": 12.0,
        "delivery_fee": 5.0,
        "tax": 1.2,
        "total_price": 18.2,
        "status": "Pending",
        "payment_status": "Pending",   # You can use this to test "Pay Now" button
        "refund_status": "None",
        "discount_applied": 0.0,
        "created_at": "2024-03-20 19:15:00"
    }
}

# ==========================================
# Feature 8: Notifications
# ==========================================
mock_notifications_db = [
    {"id": 1, "user_id": 2, "message": "Your order #1 is being prepared!", "is_read": False},
    {"id": 2, "user_id": 2, "message": "Welcome to ByteBites!", "is_read": True}
]

# ==========================================
# Feature 9: Claire's Promo Engine (Your Speciality)
# ==========================================
mock_promos_db = {
    "STUDENT5": {
        "id": 1, 
        "code": "STUDENT5", 
        "discount_value": 5.0, 
        "min_spend": 20.0, 
        "is_active": True,
        "description": "$5 off for orders over $20"
    },
    "SAVE10": {
        "id": 2, 
        "code": "SAVE10", 
        "discount_value": 10.0, 
        "min_spend": 50.0, 
        "is_active": True,
        "description": "$10 off for orders over $50"
    },
    "WELCOME": {
        "id": 3, 
        "code": "WELCOME", 
        "discount_value": 2.0, 
        "min_spend": 10.0, 
        "is_active": False, # Start as disabled to show Admin Control
        "description": "New user discount"
    }
}