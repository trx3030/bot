#!/bin/bash

# نبدأ بتثبيت المتطلبات الأساسية
pip install --upgrade pip setuptools wheel

# تثبيت المكتبات من الريكوايرمنتس
pip install -r requirements.txt

# تثبيت أدوات المتصفح الخاصة بـ Playwright
python -m playwright install

# تشغيل البوت
python outlook-telegram-bot.py
