import socket
from threading import Thread

class ConnectionManager:
    counter = 0
    def __init__(self, server_ip, port):
        self.ip = server_ip
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_threads = []
        self.turn = 1

    def start_server(self):
        self.server_socket.bind((self.ip, self.port))
        self.server_socket.listen(5)
        while True:
            client_socket, client_address = self.server_socket.accept()
            client_thread = Thread(target=self.handle_client, args=(client_socket, self.counter))
            client_thread.start()
            self.client_threads.append(client_thread)

    def handle_client(self, client_socket, counter):
        try:
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                message = data.decode("utf-8")
                if message == "Hello\n":
                    self.turn = 2
        except Exception as e:
            print(e)
        finally:
            client_socket.close()

    def stop_server(self):
        for thread in self.client_threads:
            thread.join()
        self.server_socket.close()

    def get_turn(self):
        return self.turn
