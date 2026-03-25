import csv
import os
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models.restaurant import Restaurant
from app.models.menu import MenuItem

# A simple dictionary to map food items to categories for Feature 3
# This helps us satisfy the "Filter by category" requirement
CATEGORY_MAP = {
    "Pasta": "Italian",
    "Pizza": "Italian",
    "Taccos": "Mexican",
    "Burritos": "Mexican",
    "Sushi": "Japanese",
    "Briyani rice": "Indian",
    "Salad": "Healthy",
    "Whole cake": "Dessert"
}

def ingest_kaggle_data(file_path: str):
    """
    Reads the Kaggle food_delivery.csv and puts data into our database.
    It handles both Restaurants and Menu Items.
    """
    # Create tables if they don't exist yet
    Base.metadata.create_all(bind=engine)
    
    # Open a database session
    db = SessionLocal()

    if not os.path.exists(file_path):
        print(f"Error: Could not find file at {file_path}")
        return

    try:
        with open(file_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            # Use a set to keep track of restaurant IDs we already added
            # This prevents us from adding the same restaurant 10,000 times
            added_restaurant_ids = set()

            print("--- Starting Data Ingestion ---")
            
            count = 0
            for row in reader:
                res_id = int(row['restaurant_id'])
                food_name = row['food_item']
                food_price = float(row['order_value'])

                # STEP 1: Add the Restaurant if it's new to us
                if res_id not in added_restaurant_ids:
                    # Get a category based on the food item name
                    cat = CATEGORY_MAP.get(food_name, "Other")
                    
                    # Create the restaurant object
                    new_res = Restaurant(
                        id=res_id,
                        name=f"Restaurant {res_id}",
                        category=cat
                    )
                    
                    # db.merge is safer than db.add for primary keys
                    db.merge(new_res)
                    added_restaurant_ids.add(res_id)

                # STEP 2: Add the Menu Item (Feat2-FR1)
                new_item = MenuItem(
                    name=food_name,
                    price=food_price,
                    restaurant_id=res_id
                )
                db.add(new_item)
                
                count += 1
                # Print progress every 2000 rows so we know it's working
                if count % 2000 == 0:
                    print(f"Processed {count} rows...")

            # 3. Save everything to the database
            db.commit()
            print("--- Success! ---")
            print(f"Total rows processed: {count}")
            print(f"Unique restaurants added: {len(added_restaurant_ids)}")

    except Exception as e:
        print(f"Something went wrong: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    # Make sure this path is correct inside the Docker container
    CSV_PATH = "app/data/food_delivery.csv"
    ingest_kaggle_data(CSV_PATH)