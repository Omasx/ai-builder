from fastapi import FastAPI
from pydantic import BaseModel
import uuid

app = FastAPI(title="AI App Builder")

class CreateRequest(BaseModel):
    title: str
    description: str

@app.post("/api/create")
async def create_project(req: CreateRequest):
    project_id = str(uuid.uuid4())
    return {
        "status": "success", 
        "project_id": project_id,
        "message": "Project created successfully!",
        "preview_url": f"/projects/{project_id}/"
    }

@app.get("/")
def read_root():
    return {"message": "AI App Builder is running!"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
