from flask import Flask, render_template, request
from flask_socketio import SocketIO, send
import sqlite3
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

users = {}

# ---------- DATABASE ----------
def init_db():
    conn = sqlite3.connect("chat.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            message TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_message(username, message):
    conn = sqlite3.connect("chat.db")
    c = conn.cursor()
    c.execute("INSERT INTO messages (username, message) VALUES (?, ?)", (username, message))
    conn.commit()
    conn.close()

def load_messages():
    conn = sqlite3.connect("chat.db")
    c = conn.cursor()
    c.execute("SELECT username, message FROM messages")
    data = c.fetchall()
    conn.close()
    return data
# ------------------------------

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('join')
def handle_join(username):
    users[request.sid] = username

    # send old messages to new user
    old_msgs = load_messages()
    for u, m in old_msgs:
        send(f"{u}: {m}")

@socketio.on('message')
def handle_message(msg):
    username = users.get(request.sid, "Unknown")

    save_message(username, msg)

    send(f"{username}: {msg}", broadcast=True)

@socketio.on('disconnect')
def handle_disconnect():
    users.pop(request.sid, None)

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get("PORT", 10000))
    socketio.run(app, host='0.0.0.0', port=port)
