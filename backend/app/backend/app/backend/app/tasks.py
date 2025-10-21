import uuid
from app.ai_client import AiOrchestrator
from app.store import project_status_set

def schedule_project_generation(data):
    project_id = str(uuid.uuid4())
    project_status_set(project_id, {"phase":"queued"})
    AiOrchestrator().start_full_flow(project_id, data)
    return project_id
