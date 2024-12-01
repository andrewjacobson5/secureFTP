import socket
import threading
import time

PRESENCE_PORT = 5005
PRESENCE_HOST = '0.0.0.0'  # Listen on all available network interfaces

online_users = {}  # Dictionary to track online users and their last seen time
online_users_lock = threading.Lock()  # Lock to synchronize access to online_users

# see if input user_email is online at the time
def check_online_status(user_email):
    return user_email in online_users

def start_presence_server():
    global running
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Allow port reuse
            server_socket.bind((PRESENCE_HOST, PRESENCE_PORT))  # changed so the socket binds to the predefined port. 
            port = server_socket.getsockname()[1]
            print(f"Presence server started on port {port}")
            while running:
                data, addr = server_socket.recvfrom(1024)
                if not running:
                    break
                user_email = data.decode('utf-8')
                with online_users_lock:
                    online_users[user_email] = time.time()
                print(f"Received heartbeat from {addr}")
                online_users[data.decode('utf-8')] = time.time()
    except Exception as e:
        print(f"Failed to start presence server: {e}")



def cleanup_online_users(timeout=30):
    """Periodically clean up users who haven't sent a heartbeat recently."""
    while True:
        time.sleep(10)  # Check every 10 seconds
        current_time = time.time()
        for user_email in list(online_users.keys()):
            if current_time - online_users[user_email] > timeout:
                del online_users[user_email]
                print(f"User {user_email} marked as offline due to timeout.")


# Run the presence server and cleanup thread
def run_presence_server():
    threading.Thread(target=start_presence_server, daemon=True).start()
    threading.Thread(target=cleanup_online_users, daemon=True).start()
