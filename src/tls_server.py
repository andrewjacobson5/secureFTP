import socket
import ssl
import threading
import time
import json

# Configuration
SERVER_HOST = '127.0.0.1'
TLS_PORT = 8443
TIMEOUT = 30  # Timeout in seconds to mark users as offline

CERTS_DIR = 'certs'
SERVER_CERT = f'{CERTS_DIR}/server_cert.pem'
SERVER_KEY = f'{CERTS_DIR}/server_key.pem'
CA_CERT = f'{CERTS_DIR}/ca_cert.pem'
CLIENT_CERT = f'{CERTS_DIR}/client_cert.pem'
CLIENT_KEY = f'{CERTS_DIR}/client_key.pem'

# Global dictionary to track online users and their last heartbeat timestamp
online_users = {}
# tracks which connection is which email
connected_users = {}
lock = threading.Lock()

# --- SERVER FUNCTIONS ---
def send_file(sender_sock, sender, receiver):
    try:
        receiver_sock = connected_users[reciever]
        request = "SEND_REQUEST" + sender
        receiver_sock.sendall(request.encode('utf-8'))
        dataR = receiver_sock.recv(1024)
        acpt = dataR.decode('utf-8').strip()
        if acpt == "SEND_ACCEPT":
            sender_sock.sendall(dataR)
            while True:
                dataS = sender_sock.recv(1024)
                if not dataS:
                    break
                else:
                    receiver_sock.sendall(dataS)
            complete = dataR.decode('utf-8').strip()
            if complete == "SEND_COMPLETE":
                sender_sock.sendall(complete.encode('utf-8'))
        else:
            answer = "SEND_DENIED"
            sender_sock.sendall(answer.encode('utf-8'))
    except ConnectionResetError:
        print(f"{sender} or {receiver} disconnected well sending file.\n")
    except Exception as e:
        print(f"Error sending file from {sender} to {reciever}.\n")



def handle_tls_client(conn, addr):
    # Handle a single client connection.
    print(f"Client connected {addr}")
    try:
        while True:
            time.sleep(5)
            data = conn.recv(1024)
            if not data:
                break

            # Decode the received data (user email as heartbeat)
            message = data.decode('utf-8').strip()

            #if get SEND_USER check it for an email, if the email is not online, respond so, if online grab their address
            #and send to their address a request from the sender to send a file.

            if message == "GET_USERS":
                # Respond with the online users dictionary
                with lock:
                    response = json.dumps(online_users)
                conn.sendall(response.encode('utf-8'))
            elif message[:8] == "SEND_USER":
                if message[8:] in list(online_users.keys()):
                    send_file(conn, client_email, message[8:])
                else:
                    response = "SEND_OFFLINE" + message[8:]
                    conn.sendall(response.encode('utf-8'))
            else:
                with lock:
                    client_email = message
                    online_users[client_email] = time.time()  # Update the user's last heartbeat timestamp
                    connected_users[client_email] = conn #saves the conn for sending to specific clients
    except Exception as e:
        print(f"Error handling TLS client from {addr}: {e}")
    finally:
        with lock:
            print(f"Disconnecting {addr}")
            tar = ""
            for key in connected_users:
                if connected_users[key] == conn:
                    tar = key
                    break
            del connected_users[key]
            conn.close()

def start_tls_server():
    # Start the TLS server to handle secure client connections.
    try:
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.verify_mode = ssl.CERT_REQUIRED
        context.load_cert_chain(certfile=SERVER_CERT, keyfile=SERVER_KEY)
        context.load_verify_locations(cafile=CA_CERT)

        with socket.create_server((SERVER_HOST, TLS_PORT)) as server_socket:
            with context.wrap_socket(server_socket, server_side=True) as tls_socket:
                print(f"\nServer running on {SERVER_HOST}:{TLS_PORT}")
                while True:
                    conn, addr = tls_socket.accept()
                    threading.Thread(target=handle_tls_client, args=(conn, addr, ), daemon=True).start()
        
    except Exception:
        print("Error starting TLS server")
        return


def cleanup_online_users():
    # Periodically removes users who haven't sent a heartbeat recently.
    while True:
        time.sleep(5)  # Check every 5 seconds
        current_time = time.time()

        with lock:
            for user_email in list(online_users.keys()):
                if current_time - online_users[user_email] > TIMEOUT:
                    del online_users[user_email]
                    print(f"User {user_email} marked as offline due to timeout.")


def get_online_users():
    # Retrieve the list of currently online users.
    with lock:
        return list(online_users.keys())
    

if __name__ == "__main__":
    import threading

    # Start the mutual TLS server
    print("Starting the TLS server...")
    tls_server_thread = threading.Thread(target=start_tls_server, daemon=True).start()

    # Start the cleanup thread
    threading.Thread(target=cleanup_online_users, daemon=True).start()

    # Command loop to keep the program running until the user types "exit"
    try:
        while True:
            command = input("Type 'exit' to stop the server: ").strip().lower()
            if command == "exit":
                print("Shutting down the server...")
                break
    except KeyboardInterrupt:
        print("\nServer interrupted. Shutting down.")
