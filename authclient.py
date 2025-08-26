import socket
import threading
import json
import getpass
import sys

class AuthChatClient:
    def __init__(self, host="127.0.0.1", port=5555):
        self.host = host
        self.port = port
        self.socket = None
        self.username = ""
        self.authenticated = False
        self.running = False

    def connect_to_server(self):
        """Connect to the chat server"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(10)
            self.socket.connect((self.host, self.port))
            self.socket.settimeout(None)
            print(f"🔌 Connected to server {self.host}:{self.port}")
            return True
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False

    def handle_authentication(self):
        """Handle the authentication process"""
        try:
            while not self.authenticated:
                # Receive server message
                data = self.socket.recv(1024)
                if not data:
                    return False
                
                try:
                    response = json.loads(data.decode('utf-8'))
                except json.JSONDecodeError:
                    print("❌ Invalid response from server")
                    continue
                
                if response.get("type") == "auth_required":
                    print("\n" + "="*50)
                    print("🔐 AUTHENTICATION REQUIRED")
                    print("="*50)
                    choice = self.get_auth_choice()
                    
                    if choice == "1":  # Login
                        if self.handle_login():
                            continue
                        else:
                            return False
                    elif choice == "2":  # Register
                        if self.handle_register():
                            continue
                        else:
                            return False
                    elif choice == "3":  # Exit
                        return False
                
                elif response.get("type") == "login_response":
                    if response.get("success"):
                        print(f"✅ {response.get('message')}")
                        self.authenticated = True
                        return True
                    else:
                        print(f"❌ Login failed: {response.get('message')}")
                
                elif response.get("type") == "register_response":
                    if response.get("success"):
                        print(f"✅ {response.get('message')}")
                        print("🔄 You can now login with your credentials")
                    else:
                        print(f"❌ Registration failed: {response.get('message')}")
                
                elif response.get("type") == "auth_success":
                    print(f"🎉 {response.get('message')}")
                    self.authenticated = True
                    return True
                
                elif response.get("type") == "error":
                    print(f"❌ Error: {response.get('message')}")
            
            return True
            
        except Exception as e:
            print(f"❌ Authentication error: {e}")
            return False

    def get_auth_choice(self):
        """Get user's authentication choice"""
        while True:
            print("\nChoose an option:")
            print("1. 🔑 Login")
            print("2. 📝 Register new account")
            print("3. 🚪 Exit")
            
            choice = input("\nEnter your choice (1-3): ").strip()
            
            if choice in ["1", "2", "3"]:
                return choice
            else:
                print("❌ Invalid choice. Please enter 1, 2, or 3.")

    def handle_login(self):
        """Handle user login"""
        try:
            print("\n🔑 LOGIN")
            print("-" * 20)
            username = input("Username: ").strip()
            
            if not username:
                print("❌ Username cannot be empty")
                return True  # Continue authentication loop
            
            password = getpass.getpass("Password: ")
            
            if not password:
                print("❌ Password cannot be empty")
                return True  # Continue authentication loop
            
            self.username = username
            
            # Send login request
            login_data = {
                "type": "login",
                "username": username,
                "password": password
            }
            
            self.socket.send(json.dumps(login_data).encode('utf-8'))
            return True
            
        except Exception as e:
            print(f"❌ Login error: {e}")
            return False

    def handle_register(self):
        """Handle user registration"""
        try:
            print("\n📝 REGISTER NEW ACCOUNT")
            print("-" * 30)
            username = input("Choose username (min 3 chars): ").strip()
            
            if not username:
                print("❌ Username cannot be empty")
                return True
            
            if len(username) < 3:
                print("❌ Username must be at least 3 characters long")
                return True
            
            password = getpass.getpass("Choose password (min 6 chars): ")
            
            if not password:
                print("❌ Password cannot be empty")
                return True
            
            if len(password) < 6:
                print("❌ Password must be at least 6 characters long")
                return True
            
            password_confirm = getpass.getpass("Confirm password: ")
            
            if password != password_confirm:
                print("❌ Passwords do not match")
                return True
            
            # Send registration request
            register_data = {
                "type": "register",
                "username": username,
                "password": password
            }
            
            self.socket.send(json.dumps(register_data).encode('utf-8'))
            return True
            
        except Exception as e:
            print(f"❌ Registration error: {e}")
            return False

    def receive_messages(self):
        """Receive messages from server"""
        while self.running:
            try:
                message = self.socket.recv(1024)
                if not message:
                    break
                
                decoded_message = message.decode('utf-8')
                print(f"\n{decoded_message}")
                print("> ", end="", flush=True)
                
            except OSError:
                break
            except Exception as e:
                if self.running:
                    print(f"\n❌ Error receiving message: {e}")
                break
        
        # Connection lost
        if self.running:
            print("\n⚠️ Connection lost")

    def send_messages(self):
        """Send messages to server"""
        try:
            print(f"\n💬 Welcome to the chat, {self.username}!")
            print("🔹 Type your message and press Enter")
            print("🔹 Type '/quit' or '/exit' to leave")
            print("-" * 40)
            
            while self.running:
                message = input("> ").strip()
                
                if message.lower() in ['/quit', '/exit']:
                    try:
                        self.socket.send("[leave]".encode('utf-8'))
                    except:
                        pass
                    break
                
                if message:  # Don't send empty messages
                    try:
                        self.socket.send(message.encode('utf-8'))
                    except Exception as e:
                        print(f"❌ Error sending message: {e}")
                        break

        except KeyboardInterrupt:
            print("\n🔴 Interrupted by user")
        except Exception as e:
            print(f"❌ Error in send loop: {e}")

    def start_client(self):
        """Start the chat client"""
        print("💬 Auth Chat Client")
        print("=" * 30)
        
        # Connect to server
        if not self.connect_to_server():
            return
        
        # Handle authentication
        if not self.handle_authentication():
            print("❌ Authentication failed")
            self.cleanup()
            return
        
        self.running = True
        
        # Start receive thread
        receive_thread = threading.Thread(target=self.receive_messages, daemon=True)
        receive_thread.start()
        
        # Start send loop (main thread)
        self.send_messages()
        
        # Cleanup
        self.cleanup()

    def cleanup(self):
        """Clean up resources"""
        self.running = False
        if self.socket:
            try:
                self.socket.close()
            except:
                pass
        print("🔴 Disconnected from server")

def main():
    # Optional: allow host:port override via CLI
    host = "127.0.0.1"
    port = 5555
    
    if len(sys.argv) >= 2:
        host = sys.argv[1]
    if len(sys.argv) >= 3:
        try:
            port = int(sys.argv[2])
        except ValueError:
            print("❌ Invalid port number")
            return

    client = AuthChatClient(host, port)
    client.start_client()

if __name__ == "__main__":
    main()