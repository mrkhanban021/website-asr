FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    DEBIAN_FRONTEND=noninteractive

WORKDIR /app

COPY requirements.txt /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \      
    gcc \
    g++ \
    make \
    libpq-dev \             
    libjpeg-dev \         
    zlib1g-dev \            
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*


RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /app

RUN chmod +x /app/entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]