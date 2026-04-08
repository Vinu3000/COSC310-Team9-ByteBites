mock_orders_db = {}
mock_notifications_db = []

order_id_counter = 1
notification_id_counter = 1


mock_promos_db = {
    "STUDENT5": {
        "id": 1,
        "code": "STUDENT5",
        "discount_value": 5.0,
        "min_spend": 20.0,
        "is_active": True
    },
    "SAVE10": {
        "id": 2,
        "code": "SAVE10",
        "discount_value": 10.0,
        "min_spend": 50.0,
        "is_active": True
    },
    "WELCOME": {
        "id": 3,
        "code": "WELCOME",
        "discount_value": 2.0,
        "min_spend": 10.0,
        "is_active": False  # Initialized as False to demo the Admin "Activate" button
    }
}