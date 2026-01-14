import os
import socketio
import eventlet
from flask import Flask, request, jsonify

# Gunakan async_mode='eventlet' agar WebSocket berjalan stabil di server produksi
sio = socketio.Server(cors_allowed_origins="*", async_mode='eventlet')
app = Flask(__name__)
app.wsgi_app = socketio.WSGIApp(sio, app.wsgi_app)

# Ambil key dari Environment Variable tanpa hardcode
SECRET_API_KEY = os.environ.get('MY_SECRET_KEY')

@app.route('/')
def index():
    return "NightOwl Socket.io Server is Running"

@app.route('/broadcast-status', methods=['POST'])
def broadcast_status():
    # Keamanan tambahan: Cek jika admin lupa set environment variable
    if not SECRET_API_KEY:
        return jsonify({"error": "Server configuration missing"}), 500

    client_key = request.headers.get('X-NightOwl-Key')
    if client_key != SECRET_API_KEY:
        return jsonify({"error": "Unauthorized"}), 403
    
    req_data = request.get_json()
    if not req_data:
        return jsonify({"error": "No data provided"}), 400

    # Emit data ke semua client (Electron)
    sio.emit('maintenance-update', req_data)
    return jsonify({"status": "broadcast_sent"})

@sio.event
def connect(sid, environ):
    print(f"Client connected: {sid}")

@sio.event
def disconnect(sid):
    print(f"Client disconnected: {sid}")

if __name__ == '__main__':
    # Mode development (lokal)
    import eventlet.wsgi
    port = int(os.environ.get("PORT", 5000))
    eventlet.wsgi.server(eventlet.listen(('0.0.0.0', port)), app)