FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y wget curl gnupg unzip fonts-liberation libnss3 libxss1 libasound2 libatk1.0-0 libcups2 libdbus-1-3 libgdk-pixbuf2.0-0 libgtk-3-0 libx11-xcb1 libxcomposite1 libxdamage1 libxrandr2 libgbm1 xvfb

RUN pip install playwright && python -m playwright install

COPY . .

CMD ["python", "outlook-telegram-bot.py"]