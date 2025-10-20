FROM node:18-bullseye

WORKDIR /app

RUN apt-get update && apt-get install -y python3 python3-pip

COPY . .

RUN pip3 install fastapi uvicorn requests python-dotenv redis celery

RUN cd frontend && npm install && npm run build

EXPOSE 8000

CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
