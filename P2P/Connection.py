import socket, threading, json

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
        print("########### connection.listen #########")
        self.sock.listen(1)

        #while not stop_event:
        while self.running:
            print('waiting for a connection')
            connection, client_address = self.sock.accept()
            print("ACEITOU A CONECT")
            manager = threading.Thread(target=process_request, args=(connection, client_address, timeline, server, username, vector_clock))
            manager.start()


    def stop(self):
        self.running = False
        socket.socket(socket.AF_INET, 
                  socket.SOCK_STREAM).connect((self.host, self.port))
        self.sock.close()


    # send a message to the other peer
    def send(self, msg, timeline=None):
        print("######### connection.send #########")
        try:
            self.sock.sendall(msg.encode('utf-8'))

            data = self.sock.recv(256)
            print ('received "%s"' % data.decode('utf-8'))
            if not data.decode('utf-8') == 'ACK':
                print("Foi timeline")
                info = json.loads(data)
                if info['type'] == 'timeline':
                    record_messages(data, timeline)
        finally:
            print('closing socket')
            self.sock.close()


# process the request, i.e., read the msg from socket (Thread)
def process_request(connection, client_address, timeline, server, username, vector_clock):
    print("######## connection.process_request ############3")
    
    try:
        print('connection from', client_address)
        while True:
            data = connection.recv(1024)
            #received "{"type": "timeline", "id": "a", "v_clock": {"c": 1, "a": 1}, "n": 1}"
            if data:
                print('received "%s"' % data.decode('utf-8'))
                result = process_message(data, timeline, server, username, vector_clock)
                print("######## connection.process_request ############3")
                connection.sendall(result)
                print("sé fini")
            else:
                break
    finally:
        connection.close()


def process_message(data, timeline, server, username, vector_clock):
    print("######## connection.process_message ############3")

    info = json.loads(data)
    if info['type'] == 'simple':
        timeline.append({'id': info['id'], 'message': info['msg']})
        update_vector_clock(1, info['id'], vector_clock)
        #asyncio.async(update_vector_clock(server, 1, username))
        return 'ACK'.encode('utf-8')
    elif info['type'] == 'timeline':
        print("######### typr: timeline##############3 ")
        #received "{"type": "timeline", "id": "a", "v_clock": {"c": 0, "a": 1}, "n": 1}"
        list = get_messages(info['id'], timeline, int(info['n']))
        di = {'type': 'timeline', 'list': json.dumps(list)}
        #update_vector_clock(len(list), info['id'], vector_clock)
        #asyncio.async(update_vector_clock(server, len(list), username))
        res = json.dumps(di)
        return res.encode('utf-8')
    

def update_vector_clock(n, id, vector_clock):
    print('hei')
    try:
        print("vetor_clock " )
        print(vector_clock)
        vector_clock[id] += n
        print("vetor_clock " )
        print(vector_clock)
    except Exception:
        vector_clock[id] = n
        print("vetor_clock " )
        print(vector_clock)

def get_messages(id, timeline, n):
    print("####################get_messages###################3")
    list = []
    for m in timeline:
        if m['id'] == id:
            list.append(m)
    print(list)
    print(list[-n:])
    return list[-n:]


def record_messages(data, timeline):
    info = json.loads(data)
    list = json.loads(info['list'])
    for m in list:
        timeline.append({'id': m['id'], 'message': m['message']})