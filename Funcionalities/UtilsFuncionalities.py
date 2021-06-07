from TCP.Connection import Connection
import socket

# check if a node is online
def isOnline(userIP, userPort):
    print("######### isOnline #########")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex((userIP, userPort))
    if result == 0:
        print("IS ONLINE " + userIP)
        return True
    else:
        print("NOT ONLINE " + userIP)
        return False

def send_p2p_msg(ip, port, message, timeline=None):
    print("######### send_p2p_msg #########")
    if isOnline(ip, port):
        connection = Connection(ip, port)
        connection.connect()
        connection.send(message, timeline)
        print("Enviado")
        print("SEND MESSAGE c'est FINI")