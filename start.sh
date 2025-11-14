#!/bin/bash
# =============================
# Riyad FF Info Bot Start Script
# =============================

# Upgrade pip and install dependencies
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

# Run the bot
python main.py
