from fastapi import FastAPI

app = FastAPI(title="AI App Builder")

@app.get("/")
def read_root():
    return {"message": "AI App Builder is running successfully!"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
