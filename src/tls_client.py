import socket
import ssl
import time
import json
import os.path
import threading

# Configuration
SERVER_HOST = '127.0.0.1'
TLS_PORT = 8443

CERTS_DIR = 'certs'
CA_CERT = f'{CERTS_DIR}/ca_cert.pem'
CLIENT_CERT = f'{CERTS_DIR}/client_cert.pem'
CLIENT_KEY = f'{CERTS_DIR}/client_key.pem'

lock = threading.Lock()

def connect():
    #connects the client to the server, returns the socket for use passing to other functions

    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.load_cert_chain(certfile=CLIENT_CERT, keyfile=CLIENT_KEY)
    context.load_verify_locations(cafile=CA_CERT)

    try:
        sock = socket.create_connection((SERVER_HOST, TLS_PORT))
        tls_sock = context.wrap_socket(sock, server_hostname=SERVER_HOST)
        return tls_sock, sock
    except Exception as e:
        # SERVER SHUTDOWN by one client disconnecting
        print("Error connecting to server")

def process_request(request, tls_sock):
    #processes the send file request
    try:
        with lock:
            if request[:12] == "SEND_REQUEST":
                acpt = input(f"{request[12:]} wants to send you a file. Accept (y/n)?").lower()
                if acpt != "y":
                    response = "SEND_DENIED"
                    tls_sock.sendall(response.encode('utf-8'))
                    return
                response = "SEND_ACCEPT"
                tls_sock.sendall(response.encode('utf-8'))
                dataF = tls_sock.recv(4096)
                file_name = dataF.decode('utf-8')
                with open(file_name, 'wb') as file:
                    while True:
                        data = tls_sock.recv(1024)
                        if not data:
                            break
                        else:
                            file.write(data)
                response = "SEND_COMPLETE"
                tls_sock.sendall(response.encode('utf-8'))
            else:
                print(f"Request didn't read")
    except ConnectionResetError:
        print("Disconnected from server.\n")
        #detects a disconnect, can then reconnect here if needed
    except Exception as e:
        # SERVER SHUTDOWN by one client disconnecting
        print("Error processing request")
    


def listen_request(tls_sock):
    try:
        dataR = tls_sock.recv(4096)
        request = dataR.decode('utf-8')
        print(f"{request}")
        process_request(request)
        time.sleep(5)
    except ConnectionResetError:
        print("Disconnected from server.\n")
        #detects a disconnect, can then reconnect here if needed
    except Exception as e:
        # SERVER SHUTDOWN by one client disconnecting
        print("Error listen for request")

def send_heartbeat(user_email, tls_sock):
    #sends a heartbeat
    try:
        while True:
            tls_sock.sendall(user_email.encode('utf-8'))
            time.sleep(5)  # Send heartbeat every 5 seconds
    except ConnectionResetError:
        print("Disconnected from server.\n")
        #detects a disconnect, can then reconnect here if needed
    except Exception as e:
        # SERVER SHUTDOWN by one client disconnecting
        print("Error sending heartbeat to server")

def get_online_users(tls_sock):
    # Fetch the online users dictionary from the server.
    try:
        tls_sock.sendall(b"GET_USERS")  # Send the query command
        response = tls_sock.recv(4096)  # Receive the response
        online_users = json.loads(response.decode('utf-8'))
        return online_users
    except ConnectionResetError:
        print("Disconnected from server.\n")
        #detects a disconnect, can then reconnect here if needed
    except Exception as e:
        print(f"Error fetching online users: {e}")
        return {}

def send_file(receiver, file_path, tls_sock):
    if not os.path.isfile(file_path):
        print(f"No file found.\n")
        return
    try:
        # tell the server about the recipient
        tls_sock.sendall(f"SEND_USER:{receiver}\n".encode('utf-8'))  # Send the query command
        # wait for server response
        data = tls_sock.recv(4096)  # Receive the response
        message = data.decode('utf-8').strip()
        
        if message == "SEND_OFFLINE":
            print(f"{receiver} is currently offline.\n")
        elif message == "SEND_DENIED":
            print(f"{receiver} refused the file transfer.\n")
        elif message == "SEND_ACCEPT":
            print(f"{receiver} has accepted the file transfer.\n")
            # send the file name and contents
            file_name = file_path.split('/')[-1]
            tls_sock.sendall(file_name.encode('utf-8'))
            with open(file_path, 'rb') as file:
                while chunk := file.read(1024): # changed to chunk for efficiency
                    tls_sock.sendall(chunk)
            
            # tell the server that the file is fully sent
            print("File sent. Awaiting confirmation.\n")
            tls_sock.sendall(b"SEND_COMPLETE")
            
            # handle the server's confimation
            data = tls_sock.recv(1024)
            message = data.decode('utf-8').strip()
            if message == "SEND_COMPLETE":
                print(f"The file has been successful transferred.\n")
            else:
                print(f"Error. Unexecpected response from server: {message}\n")   
            
    except ConnectionResetError:
        print("Disconnected from server.\n")
        # detects a disconnect, can then reconnect here if needed        
    except Exception as e:
        print(f"Error sending file: {e}")

def check_online_status(email, tls_sock):
    if email in get_online_users(tls_sock):
        return 1
    else: 
        return 0