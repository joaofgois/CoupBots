import socket
import threading


DEFAULT_ADDR = True  # Use default address for messages


# Client class, new instance created for each connected client
class Client(threading.Thread):
    def __init__(self, socket: socket.socket, address, id, name, signal, server: "Server"):
        threading.Thread.__init__(self)
        self.socket = socket
        self.address = address
        self.id = id
        self.name = name
        self.signal = signal
        self.server = server  # Reference to the server to forward received messages
        self.socket.settimeout(1.0)  # Set a short timeout (1 second) for recv()

    def __str__(self):
        return str(self.id) + " " + str(self.address)

    def run(self):
        while self.signal:
            try:
                data = self.socket.recv(32)
                if data:
                    # Pass the received data to the server for broadcasting
                    self.server.route_message(self, data)
                else:
                    print(f"Client {self.address} has disconnected")
                    self.signal = False
                    self.server.remove_client(self)
                    break
            except (socket.timeout, UnicodeDecodeError):
                continue
            except OSError:
                print(f"Client {self.address} has disconnected")
                self.signal = False
                self.server.remove_client(self)
                break


class Server(threading.Thread):
    def __init__(self, host="localhost", port=12345, verbose=True):
        threading.Thread.__init__(self)
        self.host = host
        self.port = port
        self.verbose = verbose
        self.socket = None
        self.signal = True
        self.connections: list[Client] = []  # Store connected clients
        self.total_connections = 0  # Count the total connections

    def setup_socket(self):
        """Setup the server socket, bind, and listen for connections."""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)
        self.socket.settimeout(1)  # Add a timeout so the accept loop can regularly check for shutdown
        self.printv(f"Server listening on {self.host}:{self.port}")

    def run(self):
        self.setup_socket()

        # Wait for new connections
        while self.signal:
            try:
                if self.socket is None:
                    self.signal = False
                    break
                sock, address = self.socket.accept()
                new_client = Client(sock, address, self.total_connections, "Name", True, self)
                self.connections.append(new_client)
                new_client.start()
                self.printv(f"New connection at ID {new_client}")
                self.total_connections += 1
            except OSError:
                continue

    def route_message(self, sender: Client, message: bytes):
        """Broadcast a message from the sender to all other connected clients."""
        self.printv(f"Broadcasting from ID {sender.id}: {message.decode('utf-8')}")
        for client in self.connections:
            if client.id != sender.id:  # Do not send the message back to the sender
                try:
                    client.socket.sendall(message)
                except OSError:
                    self.remove_client(client)

    def remove_client(self, client: Client):
        """Helper method to remove a client from the server's connection list."""
        if client in self.connections:
            self.connections.remove(client)
            self.printv(f"Client {client.address} removed from server.")

    def shutdown(self):
        """Gracefully shut down the server and all client connections."""
        self.printv("\nServer shutting down...")

        # Clean up: close the main server socket
        if self.socket:
            self.socket.close()

        # Signal all threads to finish
        self.signal = False
        self.join()

        for client in self.connections:
            client.signal = False
            client.join()

        self.printv("Server terminated.")

    def printv(self, string: str):
        if self.verbose:
            print(string)


def main():
    # Get host and port
    if DEFAULT_ADDR:
        print("Using default address for messages.")
        host = "localhost"
        port = 12345
    else:
        host = input("Host (default 'localhost'): ") or "localhost"
        port = input("Port (default '12345'): ") or "12345"
        port = int(port)  # Ensure port is an integer

    # Create server instance and start
    server = Server(host, port)
    server.start()

    try:
        while True:
            pass  # Main thread is idle, just to catch the KeyboardInterrupt
    except:
        server.shutdown()


if __name__ == "__main__":
    main()
