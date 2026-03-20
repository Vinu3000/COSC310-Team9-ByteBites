from fastapi import FastAPI
from app.database import engine, Base
from app.api.v1.auth import router as auth_router
from app.routers.items import router as items_router

# Create database tables when the app starts
Base.metadata.create_all(bind=engine)

app = FastAPI(title="ByteBites API")

app.include_router(auth_router)
app.include_router(items_router)

@app.get("/health")
def health():
    return {"status": "ok"}