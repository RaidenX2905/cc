from flask import Flask, render_template, request, redirect, url_for, flash
import os
import zipfile
import uuid

app = Flask(__name__)
app.secret_key = "secret123"

UPLOAD_FOLDER = 'static/sites'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file and file.filename.endswith('.zip'):
            unique_id = str(uuid.uuid4())
            extract_path = os.path.join(UPLOAD_FOLDER, unique_id)
            os.makedirs(extract_path, exist_ok=True)
            zip_path = os.path.join(extract_path, file.filename)
            file.save(zip_path)

            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_path)
            os.remove(zip_path)

            flash('Website uploaded and extracted!')
            return redirect(url_for('dashboard'))
        else:
            flash('Only .zip files are allowed.')
    return render_template('upload.html')

@app.route('/dashboard')
def dashboard():
    projects = os.listdir(UPLOAD_FOLDER)
    return render_template('dashboard.html', projects=projects)

@app.route('/site/<project_id>/')
def view_site(project_id):
    return redirect(url_for('static', filename=f'sites/{project_id}/index.html'))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
