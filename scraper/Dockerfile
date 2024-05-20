# Dockerfile
FROM python:3.8-slim

RUN apt-get update && \
    apt-get install -y postgresql-client && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /afrikcom

COPY requirements.txt requirements.txt
COPY scraper.py scraper.py

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "scraper.py"]
