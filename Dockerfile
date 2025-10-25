# Use official Python image as base
FROM python:3.11

RUN apt-get update --allow-releaseinfo-change && \
    apt-get install -y --no-install-recommends --fix-missing \
    wget \
    libnss3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libxss1 \
    libasound2 \
    libgbm1 \
    libgtk-3-0 \
    libx11-xcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libpangocairo-1.0-0 \
    libpango-1.0-0 \
    libxcb1 \
    libxfixes3 \
    libxrender1 \
    libxext6 \
    libx11-6 \
    libdbus-glib-1-2 \
    libdrm2 \
    libexpat1 \
    libfontconfig1 \
    libgl1 \
    libglib2.0-0 \
    libxshmfence1 \
    libxtst6 \
    libxinerama1 \
    libxkbcommon0 && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install playwright browsers AFTER pip installing playwright
RUN python -m playwright install --with-deps

COPY . .

ENV PYTHONPATH=/app/src

CMD ["python", "src/scraper.py"]