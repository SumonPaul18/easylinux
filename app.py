from flask import Flask, render_template, request, flash
import os
import subprocess

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/', methods=['GET', 'POST'])
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
    
    return render_template('index.html', output=output)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
