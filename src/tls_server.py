import socket
import ssl
import threading
import time
import queue
from utils import set_user_state


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

# tracks which connection is which email
connected_users = {}
lock = threading.Lock()
active_transfer = {}

# --- SERVER FUNCTIONS ---

def handle_tls_client(client_sock, client_email):
    """
    Handles communication with a single client.
    """
    response_queue = queue.Queue()  # Local queue for storing responses
    while True:
        file_trans = active_transfer[client_email][0]
        file_receiver_email = active_transfer[client_email][1]
        print(f"TRANS: {file_trans} | {file_receiver_email}")
        try:
            # Check for new requests from the client
            request = client_sock.recv(4096).decode('utf-8')
            if not request:
                break

            # Routes accept and deny to the original senders queue
            elif request.startswith("SEND_ACCEPT:") or request.startswith("SEND_DENY:"):
                parts = request.split(":")
                message = parts[0].strip()
                sender_email = parts[1].strip()
                receiver_email = parts[2].strip()
                sender_queue = connected_users[sender_email][1]
                sender_queue.put(message)
                if request.startswith("SEND_ACCEPT:"):
                    print(f"file transfer begining")
                    active_transfer[sender_email] = [True, receiver_email]
                    #forward_file(client_sock, connected_users[receiver_email][0])

            # Handle SEND_USER requests
            elif request.startswith("ASK_USER:"):
                parts = request.split(":")
                if len(parts) < 3:
                    print("Invalid ASK_USER format.")
                    client_sock.sendall(b"SEND_DENY")
                    continue

                sender_email = parts[1].strip()
                receiver_email = parts[2].strip()

                # Check if the receiver is online
                with lock:
                    if receiver_email not in connected_users:
                        client_sock.sendall(b"SEND_OFFLINE")
                        print(f"{receiver_email} is offline.")
                        continue

                    # Notify the receiver
                    receiver_queue = connected_users[receiver_email][1]
                    receiver_queue.put(f"SEND_REQUEST:{sender_email}")


            elif request.startswith("FILE_NAME"):
                if file_trans is True:
                    receiver_queue = connected_users[file_receiver_email][1]
                    receiver_queue.put(request)
                else:
                    print("Alert: File name sent not during file transfer")

            elif request.startswith("FILE"):
                if file_trans is True:
                    receiver_queue = connected_users[file_receiver_email][1]
                    receiver_queue.put(request)
                else:
                    print("Alert: File packet sent not during file transfer")

            elif request.startswith("END_FILE"):
                if file_trans is True:
                    receiver_queue = connected_users[file_receiver_email][1]
                    receiver_queue.put(request)
                    active_transfer[client_email] = (False, "")
                else:
                    print("Alert: File end sent not during file transfer")

            elif request.startswith("HEARTBEAT"):
                parts = request.split(":")
                if len(parts) < 2:
                    print("Invalid HEARTBEAT format.")
                    continue
                print(f"Heartbeat received from {parts[1]}\n")
                set_user_state(parts[1], 1)
            else:
                print(f"Unknown request: {request}")
        except queue.Empty:
            print(f"No response received for {client_email}.")
            client_sock.sendall(b"SEND_DENY")
        except Exception as e:
            print(f"Error handling client {client_email}: {e}")
            break
        
    # Cleanup after disconnection
    with lock:
        if client_email in connected_users:
            del connected_users[client_email]
            set_user_state(client_email, False)
            print(f"Client {client_email} removed.")


def process_client_queue(client_email):
    """
    Processes the request queue for a specific client.
    """
    client_queue = connected_users[client_email][1]
    client_sock = connected_users[client_email][0]

    while True:
        try:
            # Get the next request from the queue
            request = client_queue.get()
            print(f"QUEUE: {client_email} | {request}")
            if request.startswith("SEND_REQUEST:"):
                sender_email = request.split(":")[1].strip()

                # Notify the recipient and get their response
                try:
                    message = f"SEND_REQUEST:{sender_email}"
                    client_sock.sendall(message.encode('utf-8'))  # Send request to the recipient
                except Exception as e:
                    print(f"Error communicating with recipient {client_email}: {e}")
                    client_queue.put("SEND_DENY")  # Default to denial on error

                # Validate the response
            if request == "SEND_ACCEPT" or request == "SEND_DENY":
                try:
                    message = request
                    client_sock.sendall(message.encode('utf-8'))
                except Exception as e:
                    print(f"Error communicating with recipient {client_email}: {e}")

            if request.startswith("FILE_NAME") or request.startswith("FILE") or request.startswith("END_FILE"):
                try:
                    client_sock.sendall(request.encode('utf-8'))
                except Exception as e:
                    print(f"Error communicating file, file_name, end_file with recipient {client_email}: {e}")
            
        except Exception as e:
            print(f"Error processing queue for {client_email}: {e}")
            break




def start_tls_server():
    """
    Starts the TLS server.
    """
    
    from utils import reset_user_state
    reset_user_state()
    
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile="certs/server_cert.pem", keyfile="certs/server_key.pem")
    context.load_verify_locations(cafile="certs/ca_cert.pem")
    context.verify_mode = ssl.CERT_REQUIRED

    with socket.create_server(("127.0.0.1", 8443)) as server_sock:
        with context.wrap_socket(server_sock, server_side=True) as tls_sock:
            print("Server is running...")
                    
            while True:
                client_sock, addr = tls_sock.accept()
                client_beat = client_sock.recv(1024).decode('utf-8').strip()  # First message is the client's email
                
                parts = client_beat.split(":")
                if len(parts) < 2 and parts[0] != "HEARTBEAT":
                    print("Invalid HEARTBEAT format.")
                    continue
                
                client_email = parts[1]
                
                print(f"Client {client_email} connected from {addr}")

                # Create a queue for the client
                with lock:
                    connected_users[client_email] = (client_sock, queue.Queue())
                    active_transfer[client_email] = (False, "")

                # Start threads for handling client and queue
                threading.Thread(target=handle_tls_client, args=(client_sock, client_email), daemon=True).start()
                threading.Thread(target=process_client_queue, args=(client_email,), daemon=True).start()
                

if __name__ == "__main__":
    start_tls_server()