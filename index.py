
from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

# Ana sayfa -> login
@app.route('/')
def login():
    return render_template('login.html')

# Panel -> kategori seçimi
@app.route('/panel')
def panel():
    return render_template('panel.html')

# Repo clone mantığı (örnek)
@app.route('/clone', methods=['POST'])
def clone_repo():
    repo_url = request.form.get('repo_url')
    if repo_url:
        os.system(f"git clone {repo_url} run/")
        return f"Repo {repo_url} başarıyla çekildi!"
    return "Repo URL girilmedi."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
