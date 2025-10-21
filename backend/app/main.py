from fastapi import FastAPI
from app.api import router as api_router
from app.preview import mount_preview_routes

app = FastAPI(title="AI App Builder")
app.include_router(api_router, prefix="/api")
mount_preview_routes(app)
