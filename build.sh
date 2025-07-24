#!/bin/bash

pip install -r requirements.txt
python -m playwright install

python outlook-telegram-bot.py
