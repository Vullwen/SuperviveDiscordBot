FROM python:3.12-slim
RUN apt-get update && apt-get install -y \
    libffi-dev \
    libcairo2-dev \
    pkg-config \
    libcurl4-openssl-dev \
    build-essential \
    python3-dev

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "main.py"]
