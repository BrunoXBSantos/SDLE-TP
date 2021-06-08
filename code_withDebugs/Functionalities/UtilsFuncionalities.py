from TCP.Connection import Connection
import socket

# verify if a peer is online
def isOnline(userIP, userPort):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex((userIP, userPort))
    if result == 0:
        return True
    else:
        return False

def send_p2p_msg(ip, port, message, timeline=None):
    if isOnline(ip, port):
        connection = Connection(ip, port)
        connection.connect()
        connection.send(message, timeline)
