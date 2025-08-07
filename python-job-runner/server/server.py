
import socket
import subprocess
import json
import threading

HOST = '0.0.0.0'
PORT = 5000
AUTH_TOKEN = 'mysecrettoken'

def handle_client(conn, addr):
    print(f"[+] Connected by {addr}")
    try:
        data = conn.recv(4096)
        if not data:
            return

        request = json.loads(data.decode('utf-8'))
        token = request.get('token')
        if token != AUTH_TOKEN:
            conn.sendall(b'{"error": "Unauthorized"}')
            return

        command = request.get('job')
        if not command:
            conn.sendall(b'{"error": "No job provided"}')
            return

        try:
            result = subprocess.run(command, shell=True, text=True, capture_output=True)
            response = {
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode
            }
        except Exception as e:
            response = {"error": str(e)}

        conn.sendall(json.dumps(response).encode('utf-8'))
    finally:
        conn.close()

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"[*] Server listening on {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(conn, addr)).start()

if __name__ == "__main__":
    main()
