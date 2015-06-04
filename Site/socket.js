from socketio import SocketIO
 
# Node.js connection
sio = SocketIO()
sio.send("log_event", "PhotoPops.py started")