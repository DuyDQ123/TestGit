from flask import Flask, render_template, redirect, url_for
import subprocess
import sys

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/launch/<exercise>')
def launch_exercise(exercise):
    if exercise == 'curl':
        subprocess.Popen([sys.executable, 'curl_count.py'])
    elif exercise == 'deadlift':
        subprocess.Popen([sys.executable, 'deadlift_count.py'])
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)