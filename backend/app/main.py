from fastapi import FastAPI
from app.routers.items import router as items_router

app = FastAPI(title="ByteBites API")

app.include_router(items_router)

@app.get("/health")
def health():
    return {"status": "ok"}