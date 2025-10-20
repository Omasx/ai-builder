FROM node:18-alpine

WORKDIR /app

RUN apk add --no-cache python3 py3-pip

COPY backend ./backend/
COPY frontend ./frontend/

RUN pip3 install --no-cache-dir fastapi uvicorn requests python-dotenv redis celery

WORKDIR /app/frontend
RUN npm install --no-audit --no-fund
RUN npm run build --silent

WORKDIR /app
EXPOSE 8000
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
