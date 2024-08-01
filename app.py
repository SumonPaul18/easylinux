from flask import Flask, render_template, request
import paramiko

app = Flask(__name__)

def ssh_command(command):
    # Replace with your SSH credentials
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('192.168.106.4', username='ubuntu', password='ubuntu')

    stdin, stdout, stderr = ssh.exec_command(command)
    output = stdout.read().decode('utf-8')
    error = stderr.read().decode('utf-8')
    ssh.close()

    return output, error

@app.route('/', methods=['GET', 'POST'])
def index():
    commands = ['ls -la', 'df -h', 'free -m', 'top', 'docker ps', 'ip a', 'tail -n 15 /var/log/syslog']  # Add more commands as needed    
    output = None
    error = None
    
    if request.method == 'POST':
        command = request.form['command']
        output, error = ssh_command(command)
        #return render_template('output.html', output=output, error=error)
    return render_template('index.html', commands=commands, output=output, error=error)

if __name__ == '__main__':
    app.run(debug=True)
