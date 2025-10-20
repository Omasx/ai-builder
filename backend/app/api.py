from fastapi import APIRouter, BackgroundTasks, HTTPException
from pydantic import BaseModel
from app.tasks import schedule_project_generation
from app.store import project_status_get

router = APIRouter()

class CreateRequest(BaseModel):
    title: str
    description: str

@router.post("/create")
async def create_project(req: CreateRequest, background_tasks: BackgroundTasks):
    project_id = schedule_project_generation(req.dict())
    status = project_status_get(project_id)
    return {"status": "queued", "project_id": project_id, "detail": status}

@router.get("/status/{project_id}")
async def status(project_id: str):
    s = project_status_get(project_id)
    if not s:
        raise HTTPException(status_code=404, detail="Project not found")
    return s
