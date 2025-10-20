import os
import requests
import json
import subprocess
import re
from app.store import project_status_set

OPENROUTER_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL_WRITER = os.getenv("OPENROUTER_MODEL_WRITER")
MODEL_IMPROVER = os.getenv("OPENROUTER_MODEL_IMPROVER")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
PROJECT_BASE = "/data/projects"

class AiOrchestrator:
    def __init__(self):
        self.headers = {"Authorization": f"Bearer {OPENROUTER_KEY}", "Content-Type": "application/json"}

    def call_model(self, model, messages, timeout=120):
        payload = {"model": model, "messages": messages}
        r = requests.post(OPENROUTER_URL, headers=self.headers, json=payload, timeout=timeout)
        r.raise_for_status()
        return r.json()

    def extract_text(self, resp_json):
        try:
            return resp_json["choices"][0]["message"]["content"]
        except Exception:
            return str(resp_json)

    def parse_files_from_ai(self, text):
        pattern = r"```(?:file)?\s*([^\n]+)\n(.*?)```"
        matches = re.findall(pattern, text, flags=re.S)
        files = {}
        if matches:
            for m in matches:
                path = m[0].strip()
                content = m[1].lstrip("\n")
                files[path] = content
        else:
            files["project.txt"] = text
        return files

    def write_files(self, project_id, files):
        base = os.path.join(PROJECT_BASE, project_id)
        os.makedirs(base, exist_ok=True)
        for path, content in files.items():
            full = os.path.join(base, path)
            os.makedirs(os.path.dirname(full), exist_ok=True)
            with open(full, "w", encoding="utf-8") as f:
                f.write(content)

    def try_build_and_prepare_preview(self, project_id):
        base = os.path.join(PROJECT_BASE, project_id)
        pkg = os.path.join(base, "package.json")
        www = os.path.join(base, "www")
        os.makedirs(www, exist_ok=True)
        try:
            if os.path.exists(pkg):
                project_status_set(project_id, {"phase":"building"})
                subprocess.run(["bash","-lc", f"cd {base} && npm install --no-audit --no-fund"], check=False)
                subprocess.run(["bash","-lc", f"cd {base} && npm run build"], check=False)
                for candidate in ["build","dist","public"]:
                    src = os.path.join(base, candidate)
                    if os.path.exists(src):
                        subprocess.run(["bash","-lc", f"cp -r {src}/* {www}/ || true"], check=False)
                index = os.path.join(www, "index.html")
                if os.path.exists(index):
                    project_status_set(project_id, {"phase":"ready", "preview": f"/projects/{project_id}/"})
                    return True
            if os.path.exists(os.path.join(base, "www", "index.html")):
                project_status_set(project_id, {"phase":"ready", "preview": f"/projects/{project_id}/"})
                return True
            if os.path.exists(os.path.join(base, "project.txt")):
                content = open(os.path.join(base, "project.txt"), "r", encoding="utf-8").read()
                html = f"<html><body><pre>{content}</pre></body></html>"
                with open(os.path.join(www, "index.html"), "w", encoding="utf-8") as f:
                    f.write(html)
                project_status_set(project_id, {"phase":"ready", "preview": f"/projects/{project_id}/"})
                return True
        except Exception as e:
            project_status_set(project_id, {"phase":"error", "error": str(e)})
            return False
        project_status_set(project_id, {"phase":"failed"})
        return False

    def start_full_flow(self, project_id, data):
        try:
            project_status_set(project_id, {"phase":"creator"})
            prompt_creator = [
                {"role":"user",
                 "content": (
                     "Generate a complete project as a set of files. "
                     "Output files using code blocks in this format:\n"
                     "```file path/to/file.ext\n<file content>\n```\n"
                     "Produce a runnable frontend project if possible (React/Vite) with index.html/build output."
                     f"\n\nProject title: {data['title']}\nDescription: {data['description']}\n"
                     "Keep files small and focused. Include package.json if it's a Node project."
                 )
                }
            ]
            creator_resp = self.call_model(MODEL_WRITER, prompt_creator, timeout=180)
            initial_text = self.extract_text(creator_resp)
            files = self.parse_files_from_ai(initial_text)
            self.write_files(project_id, files)

            project_status_set(project_id, {"phase":"improver"})
            prompt_improver = [
                {"role":"user",
                 "content": (
                     "Improve the code below for production readiness: performance, accessibility, tests, "
                     "and add a build script if missing. Return the improved file set in the same file-block format.\n\n"
                     + initial_text
                 )
                }
            ]
            improver_resp = self.call_model(MODEL_IMPROVER, prompt_improver, timeout=180)
            improved_text = self.extract_text(improver_resp)
            files2 = self.parse_files_from_ai(improved_text)
            self.write_files(project_id, files2)

            project_status_set(project_id, {"phase":"finalizing"})
            prompt_final = [
                {"role":"user",
                 "content": "Finalize and produce the final project files in file-block format. Make it ready for production. " + improved_text}
            ]
            final_resp = self.call_model(MODEL_WRITER, prompt_final, timeout=180)
            final_text = self.extract_text(final_resp)
            files3 = self.parse_files_from_ai(final_text)
            self.write_files(project_id, files3)

            project_status_set(project_id, {"phase":"building"})
            ok = self.try_build_and_prepare_preview(project_id)
            if ok:
                return True
            else:
                return False
        except Exception as e:
            project_status_set(project_id, {"phase":"error", "error": str(e)})
            return False
