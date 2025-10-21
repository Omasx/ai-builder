FROM python:3.11
WORKDIR /app
COPY . .
RUN pip install fastapi uvicorn requests python-dotenv
CMD ["sh", "-c", "echo '=== File Structure ==='; pwd; ls -la; echo '=== Python Files ==='; find . -name '*.py' | head -10"]
