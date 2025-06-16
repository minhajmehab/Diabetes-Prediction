FROM python:3.12

WORKDIR /app

# Copy only the backend source code
COPY backend /app

# Copy shared files from root
COPY saved_models /app/saved_models
COPY firebase_cred.json /app/firebase_cred.json
COPY requirements.txt /app/requirements.txt
COPY .env /app/.env
COPY users.json /app/users.json

# Install dependencies
RUN pip install -r requirements.txt

# Run FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
