from flask import Flask, request
import os, subprocess, zipfile

app = Flask(__name__)

@app.route('/clone_repo', methods=['POST'])
def clone_repo():
    repo_url = request.form.get('repo_url')
    subprocess.Popen(["git", "clone", repo_url, "config/"])
    return "Repo klonlandı!"

@app.route('/upload_zip', methods=['POST'])
def upload_zip():
    zip_file = request.files['zip_file']
    path = os.path.join("config", zip_file.filename)
    zip_file.save(path)
    with zipfile.ZipFile(path, 'r') as zip_ref:
        zip_ref.extractall("config/")
    return "Zip dosyası yüklendi!"

if __name__ == '__main__':
    app.run(port=5000)
