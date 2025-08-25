import socket
import threading

# Store connected clients
clients = []

# Broadcast function -> Send message to ALL connected clients
def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:  # Don't send the message back to the sender
            try:
                client.send(message)
            except:
                clients.remove(client)  # Remove broken connections

# Handle a single client
def handle_client(client_socket, addr):
    print(f"✅ New connection from {addr}")
    while True:
        try:
            # Receive message from client
            message = client_socket.recv(1024)
            if not message:
                break

            print(f"📩 {addr} says: {message.decode()}")
            broadcast(message, client_socket)  # Send to others

        except:
            break

    # Remove client when disconnected
    print(f"❌ Connection closed from {addr}")
    clients.remove(client_socket)
    client_socket.close()

# Start the server
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("127.0.0.1", 5555))  # Localhost, port 5555
    server_socket.listen()

    print("🚀 Server started and waiting for connections...")

    while True:
        client_socket, addr = server_socket.accept()
        clients.append(client_socket)

        # Handle each client in a new thread
        thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        thread.start()

# Run the server
if __name__ == "__main__":
    start_server()
