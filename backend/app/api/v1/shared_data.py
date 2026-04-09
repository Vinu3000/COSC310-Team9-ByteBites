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
        "title": "Pizza Planet",
        "cuisine_type": "Italian",
        "category": "Italian",
        "rating": 4.5,
        "location": "UBCO North",
        "menu": [
            {"id": 101, "name": "Margherita Pizza", "price": 12.99},
            {"id": 102, "name": "Pepperoni Feast", "price": 15.50}
        ]
    },
    {
        "id": 2,
        "name": "Burger Queen",
        "title": "Burger Queen",
        "cuisine_type": "American",
        "category": "American",
        "rating": 4.2,
        "location": "UBCO South",
        "menu": [
            {"id": 201, "name": "Royal Cheese Burger", "price": 9.99},
            {"id": 202, "name": "Crispy Fries", "price": 3.50}
        ]
    },
    {
        "id": 3,
        "name": "Sushi Samurai",
        "title": "Sushi Samurai",
        "cuisine_type": "Japanese",
        "category": "Japanese",
        "rating": 4.8,
        "location": "UBCO Commons",
        "menu": [
            {"id": 301, "name": "Salmon Nigiri", "price": 5.99},
            {"id": 302, "name": "Dynamite Roll", "price": 11.00}
        ]
    },
    {
        "id": 4,
        "name": "Taco Temple",
        "title": "Taco Temple",
        "cuisine_type": "Mexican",
        "category": "Mexican",
        "rating": 4.3,
        "location": "UBCO North",
        "menu": [
            {"id": 401, "name": "Beef Tacos (3pcs)", "price": 10.50},
            {"id": 402, "name": "Fresh Guacamole", "price": 4.99}
        ]
    },
    {
        "id": 5,
        "name": "The Caffeine Club",
        "title": "The Caffeine Club",
        "cuisine_type": "Cafe",
        "category": "Cafe",
        "rating": 4.7,
        "location": "Library Level 1",
        "menu": [
            {"id": 501, "name": "Oat Milk Latte", "price": 5.25},
            {"id": 502, "name": "Blueberry Muffin", "price": 3.75}
        ]
    },
    {
        "id": 6,
        "name": "Green Garden",
        "title": "Green Garden",
        "cuisine_type": "Salad",
        "category": "Salad",
        "rating": 4.0,
        "location": "Gym Hub",
        "menu": [
            {"id": 601, "name": "Caesar Salad", "price": 11.99},
            {"id": 602, "name": "Power Protein Bowl", "price": 14.50}
        ]
    }
]

# ==========================================
# Orders
# ==========================================
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
        "status": "Preparing",
        "payment_status": "Success",
        "refund_status": "None",
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
        "payment_status": "Pending",
        "refund_status": "None",
        "discount_applied": 0.0,
        "created_at": "2024-03-20 19:15:00"
    },
    3: {
        "id": 3,
        "restaurant_name": "Sushi Samurai",
        "items": [
            {"name": "Dynamite Roll", "price": 11.0},
            {"name": "Salmon Nigiri", "price": 5.99}
        ],
        "subtotal": 16.99,
        "delivery_fee": 5.0,
        "tax": 1.70,
        "total_price": 23.69,
        "status": "Delivered",
        "payment_status": "Success",
        "refund_status": "None",
        "discount_applied": 0.0,
        "created_at": "2024-03-21 12:00:00"
    },
    4: {
        "id": 4,
        "restaurant_name": "Taco Temple",
        "items": [
            {"name": "Beef Tacos (3pcs)", "price": 10.50}
        ],
        "subtotal": 10.50,
        "delivery_fee": 5.0,
        "tax": 1.05,
        "total_price": 16.55,
        "status": "Out for Delivery",
        "payment_status": "Success",
        "refund_status": "None",
        "discount_applied": 5.0,
        "created_at": "2024-03-21 13:45:00"
    },
    5: {
        "id": 5,
        "restaurant_name": "The Caffeine Club",
        "items": [
            {"name": "Oat Milk Latte", "price": 5.25}
        ],
        "subtotal": 5.25,
        "delivery_fee": 2.0,
        "tax": 0.52,
        "total_price": 7.77,
        "status": "Cancelled",
        "payment_status": "Refunded",
        "refund_status": "Completed",
        "discount_applied": 0.0,
        "created_at": "2024-03-21 09:10:00"
    }
}

# ==========================================
# Feature 8: Notifications
# ==========================================
mock_notifications_db = [
    {
        "id": 1, 
        "user_id": 2, 
        "order_id": 1, 
        "message": "Your order #1 is being prepared!", 
        "is_read": False,
        "timestamp": "2024-03-21T18:30:00"
    },
    {
        "id": 2, 
        "user_id": 2, 
        "order_id": 2,  # Changed from None to 2 to satisfy the integer requirement
        "message": "Welcome to ByteBites!", 
        "is_read": True,
        "timestamp": "2024-03-21T09:00:00"
    }
]

# ==========================================
# Promo Engine
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
        "is_active": False,
        "description": "New user discount"
    }
}