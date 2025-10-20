from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class CreateRequest(BaseModel):
    title: str
    description: str

@router.post("/create")
async def create_project(req: CreateRequest):
    return {"status": "success", "message": "API is working"}

@router.get("/test")
async def test_api():
    return {"status": "working"}
