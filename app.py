from flask import Flask, jsonify
import os, socket
app = Flask(__name__)
@app.route('/')
def hello():
    student = os.environ.get('STUDENT_NAME', 'Student')
    return f"<h1>Hello from Jenkins CI/CD!</h1><p>Student: {student}</p><p>Host: {socket.gethostname()}</p>"
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
