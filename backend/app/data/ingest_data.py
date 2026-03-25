import csv
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models.restaurant import Restaurant
from app.models.menu import MenuItem

def ingest_kaggle_data(file_path: str):
    """
    Ingests data from the Kaggle Food Delivery CSV into the database.
    
    """
    # Create all tables defined in models if they don't exist
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()

    try:
        # Using Python's native csv module to keep the Docker image lightweight
        with open(file_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            # Use a set to track processed restaurant IDs to prevent duplicate inserts
            processed_restaurants = set()

            print("Starting data ingestion...")
            
            for row in reader:
                # Mapping Kaggle column 'restaurant_id' to our model
                res_id = int(row['restaurant_id'])
                
                # 1. Handle Restaurant Insertion
                if res_id not in processed_restaurants:
                    # 'merge' checks if the record exists; updates if yes, inserts if no
                    res = Restaurant(id=res_id, name=f"Restaurant {res_id}")
                    db.merge(res)
                    processed_restaurants.add(res_id)

                # 2. Handle Menu Item Insertion (Feat2-FR1)
                # Map 'food_item' -> name and 'order_value' -> price
                menu_item = MenuItem(
                    name=row['food_item'],
                    price=float(row['order_value']),
                    restaurant_id=res_id
                )
                db.add(menu_item)
            
            # Commit the transaction to the database
            db.commit()
            print(f"Success! Ingested data for {len(processed_restaurants)} restaurants.")

    except Exception as e:
        print(f"Error during ingestion: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    # Ensure the path matches the location inside the Docker container
    ingest_kaggle_data("app/data/food_delivery.csv")