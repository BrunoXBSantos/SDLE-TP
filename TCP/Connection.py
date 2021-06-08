import socket, threading, json
import utils

class Connection:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.running = True


    # bind an address
    def bind(self):
        server_address = (self.host, self.port)
        self.sock.bind(server_address)


    # create a connection
    def connect(self):
        server_address = (self.host, self.port)
        self.sock.connect(server_address)


    # put the socket in "Listen" mode
    def listen(self, timeline, server, username, vector_clock):
        self.sock.listen(1)
        while self.running:
            connection, client_address = self.sock.accept()
            manager = threading.Thread(target=process_request, args=(connection, client_address, timeline, server, username, vector_clock))
            manager.start()


    def stop(self):
        self.running = False
        socket.socket(socket.AF_INET, 
                  socket.SOCK_STREAM).connect((self.host, self.port))
        self.sock.close()


    # send a message to the other peer
    def send(self, msg, timeline=None):
        try:
            self.sock.sendall(msg.encode('utf-8'))
            data = self.sock.recv(256)
            print ('received "%s"' % data.decode('utf-8'))
            if not data.decode('utf-8') == 'ACK':
                info = json.loads(data)
                if info['type'] == 'timeline':
                    record_messages(data, timeline)
        finally:
            print('closing socket')
            self.sock.close()


# process the request, i.e., read the msg from socket (Thread)
def process_request(connection, client_address, timeline, server, username, vector_clock):
    try:
        while True:
            data = connection.recv(1024)
            #received "{"type": "timeline", "id": "a", "v_clock": {"c": 1, "a": 1}, "n": 1}"
            if data:
                print('received "%s"' % data.decode('utf-8'))
                result = process_message(data, timeline, server, username, vector_clock)
                connection.sendall(result)
            else:
                break
    finally:
        connection.close()


def process_message(data, timeline, server, username, vector_clock):
    info = json.loads(data)
    if info['type'] == 'simple':
        timeline.append({'id': info['id'], 'message': info['msg']})
        utils.update_vector_clock(1, info['id'], vector_clock)
        return 'ACK'.encode('utf-8')
    elif info['type'] == 'timeline':
        #received "{"type": "timeline", "id": "a", "v_clock": {"c": 0, "a": 1}, "n": 1}"
        list = get_messages(info['id'], timeline, int(info['n']))
        di = {'type': 'timeline', 'list': json.dumps(list)}
        res = json.dumps(di)
        return res.encode('utf-8')
    



def get_messages(id, timeline, n):
    list = []
    for m in timeline:
        if m['id'] == id:
            list.append(m)
    return list[-n:]


def record_messages(data, timeline):
    info = json.loads(data)
    list = json.loads(info['list'])
    for m in list:
        timeline.append({'id': m['id'], 'message': m['message']})