from mutual_cert import start_server, start_client

def run_receiver():
    print("Starting secure receiver...")
    start_server()  # Start the secure server for mutual TLS communication.

def run_sender():
    print("Starting secure sender...")
    start_client()  # Start the secure client for mutual TLS communication.
