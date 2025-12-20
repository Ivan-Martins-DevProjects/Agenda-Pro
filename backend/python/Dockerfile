FROM python:3.12-slim
WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
CMD ["gunicorn", "--reload" ,"main:app", "--bind", "0.0.0.0:8585", "--workers", "4"]

