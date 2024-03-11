from flask_socketio import SocketIO

class Socket():
    def __init__(self, app) -> None:
        self.app = app
        self.socketio = SocketIO(app, async_mode='threading')
    
        @self.socketio.on('connect')
        def handle_connect():
            print('Client connected to SocketIO')

    def start(self, **kwargs):
        self.socketio.run(self.app,**kwargs)