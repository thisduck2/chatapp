from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, emit
from datetime import datetime

app = Flask(__name__)
socketio = SocketIO(app)

# Dict: socket_id -> username
connected_users = {}

@app.route("/")
def home():
    return render_template("index.html")

@socketio.on("join")
def handle_join(data):
    username = data.get("username", "Guest")
    connected_users[request.sid] = username  # save username by session ID
    emit("user_list", list(connected_users.values()), broadcast=True)

@socketio.on("message")
def handle_message(data):
    username = data.get("username", "Guest")
    msg = data.get("msg", "")
    timestamp = datetime.now().strftime("%H:%M")
    full_msg = {"username": username, "msg": msg, "time": timestamp}
    send(full_msg, broadcast=True)

@socketio.on("disconnect")
def handle_disconnect():
    # Remove the user automatically on disconnect
    if request.sid in connected_users:
        del connected_users[request.sid]
        emit("user_list", list(connected_users.values()), broadcast=True)

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)
