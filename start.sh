#!/bin/bash
echo "🚀 Vision Bot Panel Başlatılıyor..."
echo "==================================="

# Gerekliyse son hazırlıklar
python setup.py

# Flask uygulamasını başlat
exec python index.py
