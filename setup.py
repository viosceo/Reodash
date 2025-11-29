#!/usr/bin/env python3
"""
Vision Bot Panel - Kurulum Scripti
Render, Cyclic, Railway için otomatik kurulum
"""

import os
import subprocess
import sys

def run_command(command, description):
    """Shell komutunu çalıştır ve sonucu kontrol et"""
    print(f"🚀 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, 
                              capture_output=True, text=True)
        print(f"✅ {description} tamamlandı!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} hatası: {e}")
        print(f"Stderr: {e.stderr}")
        return False

def main():
    print("🤖 Vision Bot Panel Kurulumu Başlatılıyor...")
    print("=" * 50)
    
    # Gerekli dizinleri oluştur
    directories = ["server", "projects", "temp", "templates", "static"]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"📁 {directory} dizini oluşturuldu")
    
    # Python modüllerini yükle
    if not run_command("pip install -r requirements.txt", "Modüller yükleniyor"):
        print("❌ Modül yükleme başarısız!")
        sys.exit(1)
    
    # Gerekli sistem araçlarını kontrol et (opsiyonel)
    try:
        subprocess.run(["git", "--version"], capture_output=True)
        print("✅ Git mevcut")
    except:
        print("⚠️ Git bulunamadı (opsiyonel)")
    
    # Flask uygulamasını başlat
    print("🎉 Kurulum tamamlandı! Bot paneli başlatılıyor...")
    print("=" * 50)
    
    # Flask'ı başlat
    os.system("python index.py")

if __name__ == "__main__":
    main()
