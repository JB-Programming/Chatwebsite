import socket
import threading
import time


HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_KEYWORD = "!DISCONNECT"
SERVER = "192.168.201.100"
ADDRESS = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDRESS)

class USER:
    message = ""

def send(msg):
    message_sending = msg.encode(FORMAT)
    msg_length = len(message_sending)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message_sending)
    #print(client.recv(2048).decode(FORMAT))
    #print(client.recv(2048).decode(FORMAT))

def listen_to_socket():
    while USER.message != DISCONNECT_KEYWORD:
        thread = threading.Thread(target=user_input)
        thread.start()
        incoming_message_length = int(client.recv(HEADER).decode(FORMAT))
        print(client.recv(incoming_message_length).decode(FORMAT))

def user_input():
    while USER.message != DISCONNECT_KEYWORD:
        USER.message = input()
        send(USER.message)

listen_to_socket()
