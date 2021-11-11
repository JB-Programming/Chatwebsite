import socket
import threading
from datetime import datetime


HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_KEYWORD = "!DISCONNECT"
SERVER = "172.16.1.104"
ADDRESS = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDRESS)

class USER:
    message = ""
    user_name =""

def send(msg):
    message_sending = (datetime.now().strftime('[%d/%m/%Y %H:%M:%S]') + USER.user_name + msg).encode(FORMAT)
    msg_length = len(message_sending)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message_sending)

def listen_to_socket():
    while DISCONNECT_KEYWORD not in USER.message:
        thread = threading.Thread(target=user_input)
        thread.start()
        incoming_message_length = int(client.recv(HEADER).decode(FORMAT))
        print(client.recv(incoming_message_length).decode(FORMAT))

def user_input():
    while DISCONNECT_KEYWORD not in USER.message:
        USER.message = input()
        send(USER.message)

print("Please enter your username:")
USER.user_name = input() + ": "
listen_to_socket()
