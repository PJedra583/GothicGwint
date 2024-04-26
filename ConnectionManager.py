import socket

class ConnectionManager:
    def __init__(self, server, port):
        self.server = server
        self.port = port
        self.socket = None

    def create_socket(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as msg:
            print(msg)

    def prepare_server_and_get_message(self):
        try:
            self.create_socket()
            self.socket.bind((self.server, self.port))
            self.socket.listen(1)
            conn, addr = self.socket.accept()
            from_client = ''
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                from_client += data.decode('utf-8')
            conn.close()
            return from_client
        except socket.error as msg:
            print(msg)
        return None

    def send_message_to_server(self, message):
        try:
            self.create_socket()
            self.socket.connect((self.server, self.port))
            self.socket.send(f'{message}\n'.encode())
            self.socket.close()
        except socket.error as msg:
            print(msg)



class Client:
    def __init__(self, server, port):
        self.conn_manager = ConnectionManager(server, port)

    def send_message_to_server(self, message):
        self.conn_manager.send_message_to_server(message)

# Przykładowe użycie

client = Client('127.0.0.1', 8080)
client.send_message_to_server('Hello World')
