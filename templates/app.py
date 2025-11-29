from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import os
import subprocess
import zipfile
import shutil
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

USER_DIR = "server"
PROJECTS_DIR = "projects"

# Route'ları tanımla
@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form.get('username')
    password = request.form.get('password')
    user_file = os.path.join(USER_DIR, f"{username}.txt")

    if os.path.exists(user_file):
        with open(user_file) as f:
            data = f.read()
            if f"password: {password}" in data:
                return redirect(url_for('panel'))
    
    flash("Hatalı kullanıcı adı veya şifre!", "error")
    return render_template('login.html')

@app.route('/do_register', methods=['POST'])
def do_register():
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')
    user_file = os.path.join(USER_DIR, f"{username}.txt")

    if os.path.exists(user_file):
        flash("Bu kullanıcı zaten kayıtlı!", "error")
        return render_template('register.html')
    
    with open(user_file, "w") as f:
        f.write(f"email: {email}\nusername: {username}\npassword: {password}")
    
    flash("Kayıt başarılı! Giriş yapabilirsiniz.", "success")
    return redirect(url_for('login'))

@app.route('/panel')
def panel():
    projects = []
    if os.path.exists(PROJECTS_DIR):
        for project in os.listdir(PROJECTS_DIR):
            project_path = os.path.join(PROJECTS_DIR, project)
            if os.path.isdir(project_path):
                created_time = os.path.getctime(project_path)
                projects.append({
                    'name': project,
                    'created': datetime.fromtimestamp(created_time).strftime('%d.%m.%Y %H:%M'),
                    'type': 'github' if os.path.exists(os.path.join(project_path, '.git')) else 'zip'
                })
    return render_template('panel.html', projects=projects)

@app.route('/clone_repo', methods=['POST'])
def clone_repo():
    repo_url = request.form.get('repo_url')
    project_name = request.form.get('project_name')
    
    if not repo_url:
        flash("GitHub URL'si gerekli!", "error")
        return redirect(url_for('panel'))
    
    # URL formatını düzelt
    if not repo_url.startswith(('https://', 'http://')):
        repo_url = 'https://' + repo_url
    
    if not repo_url.endswith('.git'):
        repo_url += '.git'
    
    if not project_name:
        project_name = repo_url.split('/')[-1].replace('.git', '')
    
    project_path = os.path.join(PROJECTS_DIR, project_name)
    
    if os.path.exists(project_path):
        flash("Bu proje zaten mevcut!", "error")
        return redirect(url_for('panel'))
    
    try:
        # GitHub reposunu klonla
        result = subprocess.run(['git', 'clone', repo_url, project_path], 
                              capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            # requirements.txt kontrolü
            requirements_file = os.path.join(project_path, 'requirements.txt')
            if os.path.exists(requirements_file):
                subprocess.run(['pip', 'install', '-r', requirements_file], 
                             cwd=project_path, capture_output=True)
            
            flash(f"✅ {project_name} başarıyla klonlandı!", "success")
        else:
            flash(f"❌ Klonlama hatası: {result.stderr}", "error")
            
    except Exception as e:
        flash(f"❌ Hata: {str(e)}", "error")
    
    return redirect(url_for('panel'))

@app.route('/upload_zip', methods=['POST'])
def upload_zip():
    if 'zip_file' not in request.files:
        flash("Dosya seçilmedi!", "error")
        return redirect(url_for('panel'))
    
    zip_file = request.files['zip_file']
    project_name = request.form.get('project_name')
    
    if zip_file.filename == '':
        flash("Dosya seçilmedi!", "error")
        return redirect(url_for('panel'))
    
    if not project_name:
        project_name = zip_file.filename.replace('.zip', '')
    
    project_path = os.path.join(PROJECTS_DIR, project_name)
    
    if os.path.exists(project_path):
        flash("Bu proje zaten mevcut!", "error")
        return redirect(url_for('panel'))
    
    try:
        # Geçici dosyayı kaydet ve çıkar
        temp_zip = os.path.join('temp', zip_file.filename)
        os.makedirs('temp', exist_ok=True)
        zip_file.save(temp_zip)
        
        with zipfile.ZipFile(temp_zip, 'r') as zip_ref:
            zip_ref.extractall(project_path)
        
        os.remove(temp_zip)
        
        # requirements.txt kontrolü
        requirements_file = os.path.join(project_path, 'requirements.txt')
        if os.path.exists(requirements_file):
            subprocess.run(['pip', 'install', '-r', requirements_file], 
                         cwd=project_path, capture_output=True)
        
        flash(f"✅ {project_name} başarıyla yüklendi!", "success")
        
    except Exception as e:
        flash(f"❌ ZIP hatası: {str(e)}", "error")
    
    return redirect(url_for('panel'))

if __name__ == '__main__':
    if not os.path.exists(USER_DIR):
        os.makedirs(USER_DIR)
    if not os.path.exists(PROJECTS_DIR):
        os.makedirs(PROJECTS_DIR)
    if not os.path.exists('temp'):
        os.makedirs('temp')
    
    print("🚀 Flask Sunucusu Başlatılıyor...")
    print("📡 Available Routes:")
    print("   / → login")
    print("   /login → POST login") 
    print("   /register → register")
    print("   /do_register → POST register")
    print("   /panel → panel")
    print("   /clone_repo → POST clone_repo")
    print("   /upload_zip → POST upload_zip")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
