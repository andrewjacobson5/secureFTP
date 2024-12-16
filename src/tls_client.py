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
file_path = "" #saves the file path during transfer


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
        threading.Thread(target=listener_thread, args=(email, tls_sock,), daemon=True).start()
        threading.Thread(target=process_requests, args=(tls_sock,), daemon=True).start()

        return tls_sock, sock
    except ssl.SSLError as ssl_err:
        print(f"SSL error during connection: {ssl_err}")
    except socket.error as sock_err:
        print(f"Socket error during connection: {sock_err}")
    except Exception as e:
        print(f"Unexpected error during connection: {e}")

    # Return None if connection fails
    return None, None



def listener_thread(user_email, tls_sock):
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
                    print(f"{sender_email} wants to send you a file.")
                    acpt = input(
                        "Accept? (y/n): ")
                    response = "SEND_ACCEPT" if acpt.lower() == 'y' else "SEND_DENY"
                    message = f"{response}:{sender_email}:{user_email}"
                    tls_sock.sendall(message.encode('utf-8'))
                    if response == "SEND_ACCEPT": 
                        print("Accepting file transfer")
                else:    
                    with lock:
                        request_queue.put(data)  # Add data to the queue
                        #print(f"Data added to queue: {data}")
            else:
                print("No data received. Closing producer.")
                break
    except Exception as e:
        print(f"Exception occurred in listener thread: {e}")
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
        
def process_requests(tls_sock):
    """
    Processes requests from the queue.
    Handles responses and file transfers.
    """
    file_name = ""
    file_data = ""
    while True:
        try:
            global file_path
            with lock:
                request = request_queue.get(timeout=5)  # Wait for new data (timeout after 5s)
                #print(request)
                
            if request.startswith("SEND_ACCEPT"):
                #print(file_path)
                file_name = file_path.split("/")[-1]
                print(f"File transfer accepted. Sending file {file_name}...")
                send_file(file_name, tls_sock)
                continue  # File transfer logic will follow

            elif request.startswith("SEND_DENY"):
                print("File transfer denied by the recipient.")
                continue

            elif request.startswith("SEND_OFFLINE"):
                print("Recipient is offline. File transfer aborted.")
                continue

            elif request.startswith("FILE_NAME:"):
                file_name = request.split("FILE_NAME:", 1)[1]
                print(f"receiving {file_name}")

            elif request.startswith("FILE:"):
                print("File packet")
                file_data += request.split("FILE:", 1)[1]  # Begin accumulating file data

            elif "END_FILE" in request:
                # End of file transfer
                file_data = file_data.encode('utf-8')
                save_file(file_name, file_data)  # Save the accumulated file data
                file_data = ""  # Reset for the next file
                print("File transfer completed.")

            else:
                print(f"Unhandled request: {request}")

        except :
            # queue is empty
            time.sleep(1)

def send_file(file_name, tls_sock):
    with lock:
        try:
            tls_sock.sendall(f"FILE_NAME:{file_name}".encode('utf-8'))
            with open(file_path, "rb") as file:
                while True:
                    data = file.read(1024)
                    if not data:
                        tls_sock.sendall(f"END_FILE".encode('utf-8'))
                        break
                    else:
                        tls_sock.sendall(f"FILE:{data}".encode('utf-8'))
        except Exception as e:
            print(f"Error sending file: {e}")
    
def save_file(file_name, file_data):
    """
    Saves the accumulated file data to disk.
    :param file_data: The data to write to the file.
    """
    try:
        with open(file_name, 'wb') as file:
            file.write(file_data)  # Ensure file data is in bytes
        print(f"File saved as {file_name}")
    except Exception as e:
        print(f"Error saving file: {e}")

        
def client_send_request(tls_sock, user_email):
    global file_path
    receiver = input("Enter Reciever's email: ").strip()
    file_path = input("Enter the file's path: ").strip()
    
    if not os.path.exists(file_path):
        print("Error in FTP: File does not exist.")
        file_path = ""
        return
    #print(file_path)

    with lock:
        tls_sock.sendall(f"ASK_USER:{user_email}:{receiver}".encode('utf-8'))


