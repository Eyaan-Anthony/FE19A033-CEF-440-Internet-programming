FROM python:3.11-slim

# Optional: install system deps for pillow
RUN apt-get update && apt-get install -y --no-install-recommends \
    libjpeg-dev zlib1g-dev && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy and install dependencies
COPY app/requirements.txt .
RUN pip install --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# Copy app files
COPY . .

CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]