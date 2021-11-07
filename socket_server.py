import socket
import threading


HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDRESS = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_KEYWORD = "!DISCONNECT"
DISCONNECT_MESSAGE = "You disconnected!"
DISCONNECT_MESSAGE_LENGTH = 17

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDRESS)
connected_users = []


def update_others(outgoing_message, message_length, sender):
    connected_users.remove(sender)
    for user in connected_users:
        user.send(str(message_length).encode(FORMAT))
        user.send(outgoing_message.encode(FORMAT))
    connected_users.append(sender)

def handle_client(conn, address):
    print(f"[NEW CONNECTION] {address} connected.")
    connected_users.append(conn)
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            print(f"[{address}] {msg}")
            update_others(msg,msg_length, conn)
            if DISCONNECT_KEYWORD in msg:
                connected = False
                print(f"[{address}] User disconnected!")
                conn.send(str(DISCONNECT_MESSAGE_LENGTH).encode(FORMAT))
                conn.send((DISCONNECT_MESSAGE).encode(FORMAT))

                
    connected_users.remove(conn)
    conn.close()

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, address = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, address))
        thread.start()
        print(f"[ACTIV CONNECTIONS] {threading.activeCount() - 1}")

print("[STARTING] server is starting...")
start()

