from flask import Flask, render_template, redirect, url_for, session
from auth import auth_bp
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

app.register_blueprint(auth_bp)

@app.route('/')
def index():
    if 'user' in session:
        return render_template('dashboard.html')
    return redirect(url_for('auth.login'))

@app.route('/create_project', methods=['GET', 'POST'])
def create_project():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        project_name = request.form['project_name']
        username = request.form['username']
        password = request.form['password']
        
        project_folder = os.path.join('data', project_name)
        os.makedirs(project_folder, exist_ok=True)
        
        data = {
            'username': username,
            'password': password
        }
        
        with open(os.path.join(project_folder, 'data.json'), 'w') as f:
            json.dump(data, f)
        
        return redirect(url_for('index'))
    
    return render_template('create_project.html')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
