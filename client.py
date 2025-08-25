import socket
import threading
import sys

HOST = "127.0.0.1"   # must match your server
PORT = 5555          # must match your server

def receive_messages(sock: socket.socket):
    """
    Runs in a background (daemon) thread.
    Continuously reads bytes from the socket and prints decoded messages.
    Exits when the server closes the connection or an error occurs.
    """
    while True:
        try:
            data = sock.recv(1024)  # blocking call
            if not data:
                # b'' means the remote side performed an orderly shutdown
                print("\n[system] Server closed the connection.")
                break
            print("\n" + data.decode("utf-8"), end="")
            # re-show the prompt after an incoming message
            print("\n> ", end="", flush=True)
        except OSError:
            # socket likely closed locally
            break
        except Exception as e:
            print(f"\n[error] receive thread: {e}")
            break

def send_messages(sock: socket.socket, username: str):
    """
    Runs in the main thread. Reads user input and sends it.
    '/quit' or '/exit' cleanly closes the connection.
    """
    try:
        # Announce join (server just broadcasts this text)
        sock.send(f"[join] {username} joined the chat".encode("utf-8"))

        while True:
            msg = input("> ")
            if msg.strip().lower() in ("/quit", "/exit"):
                try:
                    sock.send(f"[leave] {username} left the chat".encode("utf-8"))
                except OSError:
                    pass
                # Shutdown write side so the server sees EOF
                try:
                    sock.shutdown(socket.SHUT_WR)
                except OSError:
                    pass
                break

            # Prefix with username so others know who sent it
            wire = f"{username}: {msg}".encode("utf-8")
            sock.send(wire)

    except KeyboardInterrupt:
        print("\n[system] Ctrl+C — exiting.")
    finally:
        try:
            sock.close()
        except OSError:
            pass

def main():
    # Optional: allow host:port override via CLI: python client.py 127.0.0.1 5555
    host = HOST
    port = PORT
    if len(sys.argv) >= 2:
        host = sys.argv[1]
    if len(sys.argv) >= 3:
        port = int(sys.argv[2])

    username = input("Enter a username: ").strip() or "anon"

    # Create TCP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # (Optional) small timeout for initial connect to avoid hanging forever
    sock.settimeout(5.0)
    try:
        sock.connect((host, port))  # TCP 3-way handshake happens here
    except Exception as e:
        print(f"[error] Could not connect to {host}:{port} -> {e}")
        return
    finally:
        # After connecting, go back to blocking mode for chat I/O
        sock.settimeout(None)

    print(f"[system] Connected to {host}:{port}. Type your message and press Enter. (/quit to exit)")

    # Start the background receiver thread
    recv_thread = threading.Thread(target=receive_messages, args=(sock,), daemon=True)
    recv_thread.start()

    # Send loop stays in main thread (so input() works nicely)
    send_messages(sock, username)

    # When send loop exits, give the receiver a moment and then finish
    try:
        recv_thread.join(timeout=0.5)
    except RuntimeError:
        pass
    print("[system] Disconnected. Bye!")

if __name__ == "__main__":
    main()
