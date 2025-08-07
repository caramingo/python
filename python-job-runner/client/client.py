
import socket
import json
import sys
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout
from PyQt5.QtCore import QTimer

SERVER_HOST = 'your.server.ip'
SERVER_PORT = 5000
AUTH_TOKEN = 'mysecrettoken'

def send_job(job_command):
    request = {
        "token": AUTH_TOKEN,
        "job": job_command
    }
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((SERVER_HOST, SERVER_PORT))
        s.sendall(json.dumps(request).encode('utf-8'))
        response = s.recv(8192)
        return json.loads(response.decode('utf-8'))

def show_notification(title, message):
    app = QApplication(sys.argv)
    window = QWidget()
    window.setWindowTitle(title)
    window.setGeometry(100, 100, 400, 200)

    layout = QVBoxLayout()
    label = QLabel(message)
    label.setWordWrap(True)
    layout.addWidget(label)
    window.setLayout(layout)

    QTimer.singleShot(5000, app.quit)  # автозакрытие через 5 секунд

    window.show()
    app.exec_()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 client.py '<command>'")
        sys.exit(1)
    command = sys.argv[1]
    result = send_job(command)
    result_text = json.dumps(result, indent=2)
    show_notification("Job Result", result_text)
