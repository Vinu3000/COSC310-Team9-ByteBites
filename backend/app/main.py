from fastapi import FastAPI
from app.database import engine, Base
from app.api.v1 import auth, items, orders, restaurants
from app.api.v1.notifications import router as notifications_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="ByteBites Food Delivery API")

# Authentication -> /api/v1/auth
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])

# Menu -> /api/v1/menu
app.include_router(items.router, prefix="/api/v1/menu", tags=["Menu"])

# Restaurants -> /api/v1/restaurants 
app.include_router(restaurants.router, prefix="/api/v1/restaurants", tags=["Restaurants"])

# Orders -> /api/v1/orders
app.include_router(orders.router, prefix="/api/v1/orders", tags=["Orders"])

# Notifications -> /api/v1/notifications
app.include_router(notifications_router, prefix="/api/v1/notifications", tags=["Notifications"])

@app.get("/")
def read_root():
    return {"message": "Welcome to ByteBites API", "version": "v1.0"}