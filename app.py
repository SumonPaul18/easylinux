import paramiko
from flask import Flask, render_template, request

app = Flask(__name__)

def ssh_connect(hostname, username, pkey_file):
    try:
        transport = paramiko.Transport((hostname, 22))
        transport.connect(username=username, pkey=paramiko.RSAKey.from_private_key_file(pkey_file))
        sftp = paramiko.SFTPClient.from_transport(transport)
        return sftp, transport
    except Exception as e:
        return None, None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        hostname = request.form['hostname']
        username = request.form['username']
        pkey_file = request.form ['pkey']  # Replace with actual path
        command = request.form['command']

        sftp, transport = ssh_connect(hostname, username, pkey_file)
        if sftp:
            try:
                # Execute command or perform file operations using sftp
                stdin, stdout, stderr = transport.open_session()
                stdin.write(command + '\n')
                stdin.flush()

                output = stdout.read().decode('utf-8')
                error = stderr.read().decode('utf-8')

                # Process output and error as needed
                return render_template('result.html', output=output, error=error)
            finally:
                transport.close()
        else:
            return render_template('error.html', message='SSH connection failed')
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
