FROM python:3.11-slim

WORKDIR /app

# 1. Install system dependencies (needed for compilation)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 2. Upgrade pip (to prevent warning)
RUN pip install --upgrade pip

# 3.  PRO TRICK: Install CPU-only PyTorch (This saves 2.0 Gigabytes of download!)
RUN pip install torch --index-url https://download.pytorch.org/whl/cpu

# 4. Copy requirements and install the rest
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of the application
COPY . .

ENV PYTHONPATH=/app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]