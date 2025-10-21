FROM python:3.11
WORKDIR /app
COPY backend/ ./backend/
RUN python -m pip install fastapi uvicorn requests
CMD ["python", "-m", "uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
