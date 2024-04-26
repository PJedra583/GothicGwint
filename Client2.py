from ConnectionManager import ConnectionManager

class Client:
    def __init__(self, server, port):
        self.conn_manager = ConnectionManager(server, port)

    def send_message_to_server(self, message):
        self.conn_manager.send_message_to_server(message)
