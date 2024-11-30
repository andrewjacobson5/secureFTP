import threading
import ssl
import socket

SERVER_ADDRESS = ('localhost', 8443)
CERTS_DIR = 'certs'

SERVER_CERT = f'{CERTS_DIR}/server_cert.pem'
SERVER_KEY = f'{CERTS_DIR}/server_key.pem'
CA_CERT = f'{CERTS_DIR}/ca_cert.pem'


def start_server():
    """Start the server with support for multiple clients."""
    try:
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.verify_mode = ssl.CERT_REQUIRED
        context.load_cert_chain(certfile=SERVER_CERT, keyfile=SERVER_KEY)
        context.load_verify_locations(cafile=CA_CERT)

        # Create a socket and bind to the server address
        with socket.create_server(SERVER_ADDRESS) as server:
            with context.wrap_socket(server, server_side=True) as tls_server:
                print(f"Secure server started on {SERVER_ADDRESS}")
                while True:
                    try:
                        conn, addr = tls_server.accept()
                        print(f"Connection from {addr} established.")
                        # Start a new thread for each client
                        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()
                    except ssl.SSLError as ssl_error:
                        print(f"SSL error: {ssl_error}")
                    except Exception as e:
                        print(f"Error accepting client connection: {e}")
    except Exception as e:
        print(f"Failed to start server: {e}")

# client certificate funtion
def start_client():
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.load_cert_chain(certfile='certs/client_cert.pem', keyfile='certs/client_key.pem')
    context.load_verify_locations(cafile='certs/ca_cert.pem')

    with socket.create_connection(SERVER_ADDRESS) as sock:
        with context.wrap_socket(sock, server_hostname='localhost') as ssock:
            print('Mutual TLS server')
            ssock.sendall(b'Secure Server')

def handle_client(conn, addr):
    # Handle individual client connection.
    try:
        print(f"Handling client from {addr}")
        conn.sendall(b"Welcome to the Secure Server!")
        data = conn.recv(1024)
        if data:
            print(f"Received from client {addr}: {data.decode('utf-8')}")
    except Exception as e:
        print(f"Error handling client {addr}: {e}")
    finally:
        conn.close()
        print(f"Connection with {addr} closed.")