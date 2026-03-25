from fastapi import FastAPI
from app.database import engine, Base
from app.api.v1 import auth, items, orders
from app.models import menu, restaurant, domain

# create all our tables (users, menu, etc.)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="ByteBites Food Delivery API")

# --- Registering our features (Routers) ---

# This handles Login and Register (/auth/login)
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])

# This handles Menu items (/menu)
app.include_router(items.router, prefix="/menu", tags=["Menu & Restaurants"])
# This handles Orders
app.include_router(orders.router, prefix="/orders", tags=["Orders"])

# This is a "Hello" page when you go to the root URL
@app.get("/")
def read_root():
    """Welcome message for our M3 Demo!"""
    return {
        "message": "Welcome to ByteBites API",
        "version": "v1.0",
        "status": "Everything is working for our M3 Demo!"
    }