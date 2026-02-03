FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libxml2-dev \
    libxslt-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p models && mkdir -p database && mkdir -p data/raw && mkdir -p data/processed

EXPOSE 8000
EXPOSE 8501

CMD ["streamlit", "run", "app/main_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
