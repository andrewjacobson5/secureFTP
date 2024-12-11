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
        receiver_sock = connected_users[receiver]
        request = "\nSEND_REQUEST" + " : " + sender
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
            # Log when SEND_COMPLETE is received
            complete = receiver_sock.recv(1024).decode('utf-8').strip()
            print(f"Receiver completed file transfer with message {complete}")
            if complete == "SEND_COMPLETE":
                sender_sock.sendall(complete.encode('utf-8'))
                print(f"Sender completed file transfer with message {complete}")
            else:
                answer = "SEND_DENIED"
                sender_sock.sendall(answer.encode('utf-8'))
                
    except ConnectionResetError:
        print(f"{sender} or {receiver} disconnected well sending file.\n")
    except Exception as e:
        print(f"Error sending file from {sender} to {receiver} : {e}.\n")

def handle_tls_client(conn, addr):
    global connected_users
    global online_users
    # Handle a single client connection over TLS. 
    print(f"Client connected {addr}")
    try:
        while True:
            time.sleep(5)
            # receive the data from clint
            data = conn.recv(1024)
            if not data:
                print(f"No data received from {addr}")
                break

            # Decode the received data (user email as heartbeat)
            message = data.decode('utf-8').strip()

            #if get SEND_USER check it for an email, if the email is not online, respond so, if online grab their address
            #and send to their address a request from the sender to send a file.

            if message.startswith("SEND_USER"):
                client_email = message.split(":", 1)[1] # get the email after the prefix
            else:
                client_email = message # default
            
            if message == "GET_USERS":
                with lock:
                    response = json.dumps(online_users)
                conn.sendall(response.encode('utf-8'))
            elif message.startswith("SEND_USER"):
                target_email = message.split(":", 1)[1]
                if target_email in online_users:
                    send_file(conn, client_email, target_email)
                else:
                    conn.sendall(f"SEND_OFFLINE:{target_email}".encode('utf-8'))
            else:
                # Update online users
                with lock:
                    online_users[client_email] = time.time()
                    connected_users[client_email] = conn
    except Exception as e:
        print(f"Error handling TLS client from {addr}: {e}")
    finally:
        with lock:
            print(f"Disconnecting client {addr}")
            for key, connection in list(connected_users.items()):
                if connection == conn:
                    print(f"Removing client {key}")
                    del connected_users[key]
                    del online_users[key]
                    break
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
            to_remove = [email for email, timestamp in online_users.items() if current_time - timestamp > TIMEOUT]
            # changed the logic here, iterating over the dict's keys directly while modifying it could lead to race conditions
            # also, when `list(online_users.keys())` is called, it is recalculating each time a key is deleted.
            # iterating over `online_users.items()` only once and removing the users after avoids recalculating the keys.
            for user in to_remove:
                del online_users[user]
                print(f"User {user} marked offline due to timeout.\n")

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
