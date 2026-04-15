import eventlet
eventlet.monkey_patch()

from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)

socketio = SocketIO(
    app,
    cors_allowed_origins="*",
    async_mode="eventlet"
)

@app.route("/")
def home():
    return render_template("index.html")

@socketio.on("message")
def handle_message(msg):
    print("Received:", msg)
    socketio.emit("message", msg)  # IMPORTANT FIX

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=10000)
    @socketio.on('message')
def handle_message(data):
    username = data['username']
    message = data['message']

    print(username + ": " + message)

    send({
        'username': username,
        'message': message
    }, broadcast=True)
