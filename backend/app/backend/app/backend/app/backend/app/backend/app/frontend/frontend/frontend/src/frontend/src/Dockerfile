FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install fastapi uvicorn requests python-dotenv redis celery
RUN apt-get update && apt-get install -y curl && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && apt-get install -y nodejs
RUN cd frontend && npm install && npm run build
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
