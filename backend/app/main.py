from fastapi import FastAPI
from app.api import router as api_router

app = FastAPI(title="AI App Builder")
app.include_router(api_router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "AI App Builder is running"}
