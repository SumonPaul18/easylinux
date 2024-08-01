from flask import render_template, request, flash, redirect, url_for
from app import app
from app.utils import ssh_command

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/execute', methods=['POST'])
def execute_command():
    host = request.form['host']
    username = request.form['username']
    password = request.form['password']
    command = request.form['command']

    try:
        output, error = ssh_command(host, username, password, command)
        if error:
            flash(error, 'error')
        return render_template('index.html', output=output)
    except Exception as e:
        flash(f"An error occurred: {str(e)}", 'error')
        return redirect(url_for('index'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
