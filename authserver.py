import socket
import threading
import json
from database import DatabaseHandler

class AuthChatServer:
    def __init__(self, host="127.0.0.1", port=5555):
        self.host = host
        self.port = port
        self.clients = []
        self.authenticated_clients = {}  # Map socket to username
        self.db = DatabaseHandler()
        self.server_socket = None
        self.running = False
        
        print("🚀 Auth Chat Server initialized")
        print(f"📊 Database stats: {self.db.get_user_stats()}")

    def broadcast(self, message, sender_socket=None):
        """Send message to all authenticated clients"""
        message_bytes = message.encode('utf-8')
        
        disconnected_clients = []
        for client in self.clients:
            if client != sender_socket and client in self.authenticated_clients:
                try:
                    client.send(message_bytes)
                except:
                    disconnected_clients.append(client)
        
        # Clean up disconnected clients
        for client in disconnected_clients:
            self.remove_client(client)

    def remove_client(self, client_socket):
        """Remove client and notify others"""
        if client_socket in self.clients:
            username = self.authenticated_clients.get(client_socket, "Unknown")
            
            self.clients.remove(client_socket)
            if client_socket in self.authenticated_clients:
                del self.authenticated_clients[client_socket]
            
            if username != "Unknown":
                leave_message = f"🚪 {username} left the chat"
                self.broadcast(leave_message)
                print(f"❌ {username} disconnected")

    def handle_authentication(self, client_socket):
        """Handle user authentication process"""
        try:
            # Send welcome message
            welcome_msg = json.dumps({
                "type": "auth_required",
                "message": "Welcome! Please login or register."
            })
            client_socket.send(welcome_msg.encode('utf-8'))
            
            while True:
                data = client_socket.recv(1024)
                if not data:
                    return None
                
                try:
                    auth_data = json.loads(data.decode('utf-8'))
                except json.JSONDecodeError:
                    error_msg = json.dumps({
                        "type": "error",
                        "message": "Invalid data format"
                    })
                    client_socket.send(error_msg.encode('utf-8'))
                    continue
                
                if auth_data.get("type") == "register":
                    username = auth_data.get("username")
                    password = auth_data.get("password")
                    
                    success, message = self.db.register_user(username, password)
                    
                    response = json.dumps({
                        "type": "register_response",
                        "success": success,
                        "message": message
                    })
                    client_socket.send(response.encode('utf-8'))
                    
                    if success:
                        return username
                
                elif auth_data.get("type") == "login":
                    username = auth_data.get("username")
                    password = auth_data.get("password")
                    
                    success, message = self.db.authenticate_user(username, password)
                    
                    response = json.dumps({
                        "type": "login_response",
                        "success": success,
                        "message": message
                    })
                    client_socket.send(response.encode('utf-8'))
                    
                    if success:
                        return username
                
                else:
                    error_msg = json.dumps({
                        "type": "error",
                        "message": "Unknown request type"
                    })
                    client_socket.send(error_msg.encode('utf-8'))
        
        except Exception as e:
            print(f"❌ Authentication error: {e}")
            return None

    def handle_client(self, client_socket, addr):
        """Handle authenticated client messages"""
        print(f"🔌 New connection from {addr}")
        
        # First, authenticate the user
        username = self.handle_authentication(client_socket)
        
        if username is None:
            print(f"❌ Authentication failed for {addr}")
            client_socket.close()
            if client_socket in self.clients:
                self.clients.remove(client_socket)
            return
        
        # User is now authenticated
        self.authenticated_clients[client_socket] = username
        
        # Send success message
        success_msg = json.dumps({
            "type": "auth_success",
            "message": f"Welcome to the chat, {username}!"
        })
        client_socket.send(success_msg.encode('utf-8'))
        
        # Notify others
        join_message = f"👋 {username} joined the chat"
        self.broadcast(join_message, client_socket)
        print(f"✅ {username} authenticated and joined from {addr}")
        
        # Handle regular chat messages
        try:
            while self.running:
                message = client_socket.recv(1024)
                if not message:
                    break
                
                decoded_message = message.decode('utf-8')
                
                if decoded_message.startswith("[leave]"):
                    break
                else:
                    # Regular chat message - add username prefix
                    chat_message = f"{username}: {decoded_message}"
                    print(f"📩 {chat_message}")
                    self.broadcast(chat_message, client_socket)

        except Exception as e:
            print(f"❌ Error handling client {addr}: {e}")
        finally:
            self.remove_client(client_socket)
            client_socket.close()

    def start_server(self):
        """Start the authentication-enabled chat server"""
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            self.running = True

            print(f"🚀 Auth Chat Server started on {self.host}:{self.port}")
            print("🔐 Authentication required for all users")
            print("=" * 50)

            while self.running:
                try:
                    client_socket, addr = self.server_socket.accept()
                    self.clients.append(client_socket)

                    # Create thread for each client
                    thread = threading.Thread(
                        target=self.handle_client, 
                        args=(client_socket, addr),
                        daemon=True
                    )
                    thread.start()
                    
                except OSError:
                    if self.running:
                        print("Server socket closed")
                    break

        except Exception as e:
            print(f"❌ Server error: {e}")
        finally:
            self.stop_server()

    def stop_server(self):
        """Stop the server and close all connections"""
        print("\n🛑 Shutting down server...")
        self.running = False
        
        # Close all client connections
        for client in self.clients[:]:
            try:
                client.close()
            except:
                pass
        
        # Close server socket
        if self.server_socket:
            try:
                self.server_socket.close()
            except:
                pass
        
        print("✅ Server stopped successfully")

def main():
    server = AuthChatServer()
    try:
        server.start_server()
    except KeyboardInterrupt:
        print("\n🔴 Server interrupted by user")
        server.stop_server()

if __name__ == "__main__":
    main()