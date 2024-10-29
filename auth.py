from flask import Blueprint, render_template, request, redirect, url_for, session
import smtplib
import random

auth_bp = Blueprint('auth', __name__)

users = {}

def send_verification_code(email):
    code = random.randint(100000, 999999)
    users[email] = {'code': code}
    # Here you would send the email with the code
    print(f"Verification code sent to {email}: {code}")

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        code = request.form['code']
        
        if email in users and users[email]['code'] == int(code):
            session['user'] = email
            return redirect(url_for('index'))
        else:
            return "Invalid code or email"
    
    return render_template('login.html')

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        send_verification_code(email)
        return redirect(url_for('auth.login'))
    
    return render_template('signup.html')
