FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y curl

COPY backend/ ./backend/

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir fastapi uvicorn requests python-dotenv

EXPOSE 8000

CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
