from ConnectionManager import ConnectionManager

class Server:
    def __init__(self, server, port):
        self.conn_manager = ConnectionManager(server, port)

    def prepare_server_and_get_message(self):
        return self.conn_manager.prepare_server_and_get_message()

    server =('127.0.0.1', 8080)
    print(server.prepare_server_and_get_message())
