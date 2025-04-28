FROM nikolaik/python-nodejs:python3.12-nodejs18-slim

RUN apt-get update && apt-get install -y \
    chromium \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libatspi2.0-0 \
    libcups2 \
    libdbus-1-3 \
    libdrm2 \
    libgbm1 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libwayland-client0 \
    libxcomposite1 \
    libxdamage1 \
    python3-tk python3-dev \
    libxfixes3 \
    wget \
    gnupg2 \
    lsof \
    apt-transport-https \
    ca-certificates \
    x11-utils \
    xdg-utils \
    xvfb \
    software-properties-common \
    curl \
    && rm -rf /var/lib/apt/lists/*

ENV CHROME_BIN=/usr/bin/chromium

ENV PYTHONUNBUFFERED=1

RUN mkdir app
WORKDIR /app
COPY cloudflare-bypasser.py /app


RUN python -m pip install --upgrade botasaurus
RUN pip install pyautogui uvicorn fastapi

EXPOSE 8000

CMD ["python", "cloudflare-bypasser.py"]