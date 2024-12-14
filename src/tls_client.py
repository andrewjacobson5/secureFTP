import socket
import ssl
import time
import os
import threading
from queue import Queue, Empty

# Configuration
SERVER_HOST = '127.0.0.1'
TLS_PORT = 8443

CERTS_DIR = 'certs'
CA_CERT = f'{CERTS_DIR}/ca_cert.pem'
CLIENT_CERT = f'{CERTS_DIR}/client_cert.pem'
CLIENT_KEY = f'{CERTS_DIR}/client_key.pem'

lock = threading.Lock()  # Ensures thread-safe access to the TLS socket
request_queue = Queue()  # Queue to handle specific server responses


def connect(email):
    """
    Connects the client to the server using mutual TLS, returns the TLS socket and raw socket.
    
    :param email: The email of the client (used for heartbeats).
    :return: TLS socket and raw socket if successful, otherwise (None, None).
    """
    # Create a TLS context for mutual authentication
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    try:
        # Load the client's certificate and private key
        context.load_cert_chain(certfile=CLIENT_CERT, keyfile=CLIENT_KEY)

        # Load the CA certificate for verifying the server
        context.load_verify_locations(cafile=CA_CERT)

        # Connect to the server
        print(f"Connecting to {SERVER_HOST}:{TLS_PORT} with email {email}...")
        sock = socket.create_connection((SERVER_HOST, TLS_PORT))
        tls_sock = context.wrap_socket(sock, server_hostname=SERVER_HOST)
        print("Connected to the server with TLS.")

        # Start background tasks
        threading.Thread(target=send_heartbeat, args=(email, tls_sock), daemon=True).start()
        threading.Thread(target=listener_thread, args=(tls_sock,), daemon=True).start()
        threading.Thread(target=process_requests, daemon=True).start()

        return tls_sock, sock
    except ssl.SSLError as ssl_err:
        print(f"SSL error during connection: {ssl_err}")
    except socket.error as sock_err:
        print(f"Socket error during connection: {sock_err}")
    except Exception as e:
        print(f"Unexpected error during connection: {e}")

    # Return None if connection fails
    return None, None



def listener_thread(tls_sock):
    try:
        while True:
            data = tls_sock.recv(4096).decode('utf-8')
            if data:
                if data.startswith("SEND_REQUEST"):
                    parts = data.split(":", 1)
                    if len(parts) < 2:
                        print("Invalid SEND_REQUEST format.\n")
                        return

                    sender_email = parts[1].strip()
                    acpt = input(
                        f"{sender_email} wants to send you a file. Accept? (y/n): ")
                    response = "SEND_ACCEPT" if acpt.lower() == 'y' else "SEND_DENIED"
                    tls_sock.sendall(response.encode('utf-8'))
                    
                with lock:
                    request_queue.put(data)  # Add data to the queue
                    print(f"Data added to queue: {data}")
            else:
                print("No data received. Closing producer.")
                break
    except:
        print("Exception occurred in listener thread")
        return


def send_heartbeat(user_email, tls_sock):
    # Sends a periodic heartbeat to the server
    try:
        while True:
            with lock:
                tls_sock.sendall(f"HEARTBEAT:{user_email}".encode('utf-8'))
            time.sleep(5)  # Send heartbeat every 5 seconds
    except Exception as e:
        print(f"Error sending heartbeat: {e}")
        
def process_requests():
    """
    Processes requests from the queue.
    Handles responses and file transfers.
    """
    file_data = ""
    while True:
        try:
            with lock:
                request = request_queue.get(timeout=5)  # Wait for new data (timeout after 5s)
                
            if request.startswith("SEND_ACCEPT"):
                print("File transfer accepted. Receiving file...")
                continue  # File transfer logic will follow

            elif request.startswith("SEND_DENY"):
                print("File transfer denied by the recipient.")
                continue

            elif request.startswith("SEND_OFFLINE"):
                print("Recipient is offline. File transfer aborted.")
                continue

            elif request.startswith("START_FILE"):
                print("File transfer initiated.")
                file_data = request.split("START_FILE:", 1)[1]  # Begin accumulating file data

            elif "END_FILE" in request:
                # End of file transfer
                file_data += request.split(":END_FILE", 1)[0]
                save_file(file_data)  # Save the accumulated file data
                file_data = ""  # Reset for the next file
                print("File transfer completed.")

            else:
                print(f"Unhandled request: {request}")

        except :
            # queue is empty
            time.sleep(1)

    
    
def save_file(file_data):
    """
    Saves the accumulated file data to disk.
    :param file_data: The data to write to the file.
    """
    file_name = "received_file.bin"
    with open(file_name, 'wb') as file:
        file.write(file_data.encode('utf-8'))  # Ensure file data is in bytes
    print(f"File saved as {file_name}")

        
def client_send_request(tls_sock, user_email):
    receiver = input("Enter Reciever's email: ").strip()
    file_path = input("Enter the file's path: ").strip()
    
    if not os.path.exists(file_path):
        print("Error in FTP: File does not exist.")
        return
    
    with lock:
        tls_sock.sendall(f"ASK_USER:{user_email}:{receiver}".encode('utf-8'))

