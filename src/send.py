from tls_client import send_file


def send(tls_sock):
    reciever = input("Enter Reciever's email: ").strip()
    file_path = input("Enter the file's path: ").strip()
    send_file(reciever, file_path, tls_sock)
