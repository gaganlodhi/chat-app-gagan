from flask import Flask, render_template, request
from flask_socketio import SocketIO, send
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

users = {}

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('join')
def handle_join(username):
    users[request.sid] = username

@socketio.on('message')
def handle_message(msg):
    username = users.get(request.sid, "Unknown")
    full_msg = f"{username}: {msg}"
    print(full_msg)
    send(full_msg, broadcast=True)

@socketio.on('disconnect')
def handle_disconnect():
    users.pop(request.sid, None)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host='0.0.0.0', port=port, debug=True)
