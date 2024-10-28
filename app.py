from flask import Flask, render_template, request, flash, session, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import os
import subprocess
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# OAuth setup
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id='36805900645-goeo9gp0cnlsgbmpp8ssec7fvhcgt3nq.apps.googleusercontent.com',
    client_secret='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',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    access_token_params=None,
    refresh_token_url=None,
    redirect_uri='http://localhost:5000/login/callback',
    client_kwargs={'scope': 'openid profile email'}
)

github = oauth.register(
    name='github',
    client_id='YOUR_GITHUB_CLIENT_ID',
    client_secret='YOUR_GITHUB_CLIENT_SECRET',
    access_token_url='https://github.com/login/oauth/access_token',
    authorize_url='https://github.com/login/oauth/authorize',
    authorize_params=None,
    access_token_params=None,
    client_kwargs={'scope': 'user:email'}
)

# User model
class User(UserMixin):
    def __init__(self, id, name, email):
        self.id = id
        self.name = name
        self.email = email

@login_manager.user_loader
def load_user(user_id):
    return User(user_id, session.get('user_name'), session.get('user_email'))

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login/google')
def login_google():
    redirect_uri = url_for('authorize_google', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/login/github')
def login_github():
    redirect_uri = url_for('authorize_github', _external=True)
    return github.authorize_redirect(redirect_uri)

@app.route('/login/callback')
def authorize_google():
    token = google.authorize_access_token()
    resp = google.get('userinfo')
    user_info = resp.json()
    user = User(user_info['sub'], user_info['name'], user_info['email'])
    login_user(user)
    session['user_name'] = user_info['name']
    session['user_email'] = user_info['email']
    return redirect('/')

@app.route('/github/callback')
def authorize_github():
    token = github.authorize_access_token()
    resp = github.get('user')
    user_info = resp.json()
    user = User(user_info['id'], user_info['login'], user_info['email'])
    login_user(user)
    session['user_name'] = user_info['login']
    session['user_email'] = user_info['email']
    return redirect('/')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('user_name', None)
    session.pop('user_email', None)
    return redirect('/')

@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    output = None
    if request.method == 'POST':
        input1 = request.form['input1']
        input2 = request.form['input2']
        input3 = request.form['input3']
        
        folder_name = 'data_folder'
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        
        file_path = os.path.join(folder_name, 'data.txt')
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(f'NAME="{input1}"\n')
            file.write(f'EMAIL="{input2}"\n')
            file.write(f'DEPT="{input3}"\n')
        
        # run shell script
        script_path = './shell.sh'
        result = subprocess.run(['bash', script_path, input1, input2, input3], capture_output=True, text=True)
        output = result.stdout
        
        flash('Data saved successfully!')
        
        # Store output in session
        session['output'] = output
        
        # Clear data.txt file after processing
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write('')
    
    # Retrieve output from session and clear it
    output = session.pop('output', None)
    
    return render_template('index.html', output=output)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
