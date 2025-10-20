from fastapi import HTTPException
from fastapi.responses import FileResponse
import os

BASE_DIR = "/data/projects"

def mount_preview_routes(app):
    @app.get("/projects/{project_id}")
    def project_index(project_id: str):
        base = os.path.join(BASE_DIR, project_id, "www")
        index = os.path.join(base, "index.html")
        if os.path.exists(index):
            return FileResponse(index)
        else:
            raise HTTPException(status_code=404, detail="Preview not ready or index.html missing")

    @app.get("/projects/{project_id}/{path:path}")
    def project_file(project_id: str, path: str):
        base = os.path.join(BASE_DIR, project_id, "www")
        file_path = os.path.join(base, path)
        if os.path.exists(file_path) and os.path.commonpath([os.path.abspath(file_path), base]) == os.path.abspath(base):
            return FileResponse(file_path)
        else:
            raise HTTPException(status_code=404, detail="File not found")
