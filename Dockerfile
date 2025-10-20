FROM python:3.11-slim

WORKDIR /app

RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir fastapi uvicorn requests python-dotenv redis

COPY backend/ ./backend/

EXPOSE 8000

CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
