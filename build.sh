#!/bin/bash

# تحديث pip وأدوات البناء
pip install --upgrade pip setuptools wheel

# تثبيت المتطلبات
pip install -r requirements.txt

# تثبيت playwright وتهيئة المتصفح
playwright install --with-deps
