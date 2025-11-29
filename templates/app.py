from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
import os
import subprocess
import threading
import time
from datetime import datetime
import shutil

app = Flask(__name__)
app.secret_key = 'supersecretkey123'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

USER_DIR = "server"
PROJECTS_DIR = "projects"

@app.before_request
def require_login():
    if request.endpoint not in ['login', 'do_login', 'register', 'do_register'] and 'username' not in session:
        return redirect(url_for('login'))

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form.get('username')
    password = request.form.get('password')
    user_file = os.path.join(USER_DIR, f"{username}.txt")

    if os.path.exists(user_file):
        with open(user_file) as f:
            data = f.read()
            if f"password: {password}" in data:
                session['username'] = username
                user_project_dir = os.path.join(PROJECTS_DIR, username)
                os.makedirs(user_project_dir, exist_ok=True)
                flash("Başarıyla giriş yapıldı!", "success")
                return redirect(url_for('panel'))
    
    flash("Hatalı kullanıcı adı veya şifre!", "error")
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

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
    
    user_project_dir = os.path.join(PROJECTS_DIR, username)
    os.makedirs(user_project_dir, exist_ok=True)
    
    flash("Kayıt başarılı! Giriş yapabilirsiniz.", "success")
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash("Çıkış yapıldı!", "info")
    return redirect(url_for('login'))

@app.route('/panel')
def panel():
    username = session.get('username')
    user_projects_dir = os.path.join(PROJECTS_DIR, username)
    
    projects = []
    if os.path.exists(user_projects_dir):
        for project in os.listdir(user_projects_dir):
            project_path = os.path.join(user_projects_dir, project)
            if os.path.isdir(project_path):
                files = []
                for file in os.listdir(project_path):
                    if file.endswith('.py'):
                        files.append(file)
                
                created_time = os.path.getctime(project_path)
                projects.append({
                    'name': project,
                    'files': files,
                    'created': datetime.fromtimestamp(created_time).strftime('%d.%m.%Y %H:%M')
                })
    
    return render_template('panel.html', username=username, projects=projects)

@app.route('/upload_python', methods=['POST'])
def upload_python():
    username = session.get('username')
    project_name = request.form.get('project_name')
    
    if not project_name:
        flash("Proje adı gerekli!", "error")
        return redirect(url_for('panel'))
    
    if 'python_files' not in request.files:
        flash("Dosya seçilmedi!", "error")
        return redirect(url_for('panel'))
    
    files = request.files.getlist('python_files')
    user_project_dir = os.path.join(PROJECTS_DIR, username, project_name)
    
    os.makedirs(user_project_dir, exist_ok=True)
    
    uploaded_files = []
    for file in files:
        if file and file.filename.endswith('.py'):
            file_path = os.path.join(user_project_dir, file.filename)
            file.save(file_path)
            uploaded_files.append(file.filename)
    
    if uploaded_files:
        flash(f"✅ {len(uploaded_files)} Python dosyası başarıyla yüklendi!", "success")
    else:
        flash("❌ Geçerli Python dosyası bulunamadı!", "error")
    
    return redirect(url_for('panel'))

@app.route('/get_file_content/<project_name>/<filename>')
def get_file_content(project_name, filename):
    username = session.get('username')
    file_path = os.path.join(PROJECTS_DIR, username, project_name, filename)
    
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return jsonify({'success': True, 'content': content})
    else:
        return jsonify({'success': False, 'error': 'Dosya bulunamadı'})

@app.route('/save_file/<project_name>/<filename>', methods=['POST'])
def save_file(project_name, filename):
    username = session.get('username')
    file_path = os.path.join(PROJECTS_DIR, username, project_name, filename)
    
    content = request.json.get('content', '')
    
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/run_project/<project_name>')
def run_project(project_name):
    username = session.get('username')
    user_project_dir = os.path.join(PROJECTS_DIR, username, project_name)
    
    python_files = [f for f in os.listdir(user_project_dir) if f.endswith('.py')]
    
    if not python_files:
        flash("❌ Çalıştırılacak Python dosyası bulunamadı!", "error")
        return redirect(url_for('panel'))
    
    main_file = None
    for preferred in ['main.py', 'app.py', 'bot.py', 'run.py']:
        if preferred in python_files:
            main_file = preferred
            break
    
    if not main_file:
        main_file = python_files[0]
    
    try:
        process = subprocess.Popen(
            ['python', main_file],
            cwd=user_project_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        def get_output():
            output, error = process.communicate()
            if output:
                flash(f"✅ {project_name} çıktısı: {output}", "success")
            if error:
                flash(f"⚠️ {project_name} hatası: {error}", "warning")
        
        threading.Thread(target=get_output).start()
        flash(f"✅ {project_name} başlatıldı!", "success")
        
    except Exception as e:
        flash(f"❌ Hata: {str(e)}", "error")
    
    return redirect(url_for('panel'))

@app.route('/delete_project/<project_name>')
def delete_project(project_name):
    username = session.get('username')
    user_project_dir = os.path.join(PROJECTS_DIR, username, project_name)
    
    if os.path.exists(user_project_dir):
        shutil.rmtree(user_project_dir)
        flash("✅ Proje silindi!", "success")
    else:
        flash("❌ Proje bulunamadı!", "error")
    
    return redirect(url_for('panel'))

if __name__ == '__main__':
    if not os.path.exists(USER_DIR):
        os.makedirs(USER_DIR)
    if not os.path.exists(PROJECTS_DIR):
        os.makedirs(PROJECTS_DIR)
    
    print("🚀 Vision Bot Panel Başlatılıyor...")
    print("📡 Routes:")
    for rule in app.url_map.iter_rules():
        print(f"   {rule.rule} -> {rule.endpoint}")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
