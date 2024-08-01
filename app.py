from flask import Flask, render_template, request
import paramiko

app = Flask(__name__)

def ssh_command(ip_address, username, password, command):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip_address, username=username, password=password)

    stdin, stdout, stderr = ssh.exec_command(command)
    output = stdout.read().decode('utf-8')
    error = stderr.read().decode('utf-8')
    ssh.close()

    return output, error

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        ip_address = request.form['ip_address']
        username = request.form['username']
        password = request.form['password']  # Securely handle passwords
        command = request.form['command']

        output, error = ssh_command(ip_address, username, password, command)
        return render_template('output.html', output=output, error=error)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
