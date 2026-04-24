from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import time
import threading
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'rkraja'
socketio = SocketIO(app, cors_allowed_origins="*")

groups = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/configure', methods=['POST'])
def configure():
    cookies = request.form.get('cookies')
    prefix = request.form.get('prefix')
    admin_id = request.form.get('adminID')

    try:
        appstate = json.loads(cookies)
    except:
        return "❌ Invalid JSON!"

    socketio.emit('botlog', f'✅ Bot Started with Prefix: {prefix}')
    socketio.emit('botlog', f'👑 Admin ID: {admin_id}')

    # Dummy bot thread (simulation)
    def bot_run():
        global groups
        groups = ['1234567890', '9876543210']  # demo group IDs
        
        socketio.emit('groupsUpdate', groups)

        for i in range(10):
            socketio.emit('botlog', f'🤖 Running task {i+1}...')
            time.sleep(2)

        socketio.emit('botlog', '✅ Bot Finished Work!')

    threading.Thread(target=bot_run).start()

    return "🚀 Bot Started Successfully!"

@socketio.on('connect')
def handle_connect():
    emit('botlog', '🔌 Connected to server')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
