import argparse
import asyncio
from asyncio.runners import run
import json
from logging import error
import random
import sys, socket

from threading import Thread
from P2P.Connection import Connection
from P2P.Connection import update_vector_clock
import builder
from Menu.Menu import Menu
import Menu.Menu as menu
import async_tasks
from Storage import storage

from kademlia.network import Server


# -- Global VARS --
queue = asyncio.Queue()
p2p_port = ""
username = ""
ip_address = ""
timeline = []
following = []
vector_clock = {}
db_file = 'db'


# get the username
def get_username():
    nick = input('username: ')
    return nick.replace('\n', '')


# follow a user. After, he can be found in the list "following"
async def follow_user():
    user = input('User username: ')
    user_id = user.replace('\n', '')
    
    result = await server.get(user_id)

    if result is None:
        print('That user doesn\'t exist!')
    else:
        userInfo = json.loads(result)
        print(userInfo)
        try:
            if userInfo['followers'][username]:
                print('You\'re following him!')

        except Exception as err:
            following.append({'id': user_id, 'ip': userInfo['ip'], 'port': userInfo['port']})
            userInfo['followers'][username] = f'{ip_address} {p2p_port}'
            userInfo['vector_clock'][username] = 0
            asyncio.ensure_future(server.set(user_id, json.dumps(userInfo)))
            print(await (server.get(user_id)))
            return True
    return True


# show own timeline
async def show_timeline():
    menu.clear_screen()
    print('_______________ Timeline _______________')
    print("")
    for m in timeline:
        print(m['id'] + ' - ' + m['message'])
    print("")
    print('________________________________________')
    input('Press Enter')
    menu.clear_screen()
    return False


# send message to the followers
async def send_msg():
    print("######### send_msg #########")
    msg = input('Insert message: ')
    msg = msg.replace('\n','')
    timeline.append({'id': username, 'message': msg})
    print(msg)
    result = builder.simple_msg(msg, username)
    await (async_tasks.task_send_msg(result, server, username, vector_clock))
    return False


# exit app
def exit_loop():
    return True

# check if the number of args is valid
def check_argv():
    if len(sys.argv) < 3:
        print("Usage: python peer.py <-pDHT port_dht> <-pP2P port_p2p> [<-ipB bootstrap_ip> <-pB bootstrap_port>]")
        sys.exit(1)

# Get user real ip
def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip


# get the username
def get_username():
    nick = input('username: ')
    return nick.replace('\n', '')

# put the peer in "Listen mode" for new connections
def start_p2p_listenner(connection):
    print("########### start_p2p_listenner ##########")
    connection.bind()
    connection.listen(timeline, server, username, vector_clock)

# handler process IO request
def handle_stdin():
    data = sys.stdin.readline()
    asyncio.ensure_future(queue.put(data)) # Queue.put is a coroutine, so you can't call it directly.


# build a json with user info and put it in the DHT
async def build_user_info(username):
    exists = await server.get(username)
    print(exists)    #check if user exists in DHT
    if exists is None:
        info = builder.user_info(username, ip_address, p2p_port)
        vector_clock[username] = 0
        await (server.set(username, info))


def parse_arguments():
    parser = argparse.ArgumentParser()
    # Optional arguments
    parser.add_argument("-ipB", "--ipB", help="IP address of Bootstrap node", type=str, default="0.0.0.0")
    parser.add_argument("-pB", "--pB", help="port number of Bootstrap node", type=int, default=2000)
    parser.add_argument("-pDHT", "--pDHT", help="UDP port", type=int, default=None)
    parser.add_argument("-pP2P", "--pP2P", help="TCP port", type=int, default=None)
    return parser.parse_args()


# get timeline to the followings TODO
async def get_timeline():
    print("################## get_timeline #################")
    result2 = await server.get(username) # obtenho o json do 'c'
    print(result2)
    ownInfo = json.loads(result2)
    for user in following:
        #estou no c, o 'c' segue o 'a' e o 'b'
        # following: [{'id': 'a', 'ip': '192.168.1.82', 'port': 5001}, {'id': 'b', 'ip': '192.168.1.82', 'port': 6001}]
        # user: {'id': 'a', 'ip': '192.168.1.82', 'port': 5001}
        result = await server.get(user['id']) # obtenho o json do 'a'
        print("result")
        # {"ip": "192.168.1.82", "port": 5001, "followers": {"c": "192.168.1.82 7001", "b": "192.168.1.82 6001"}, "vector_clock": {"a": 2, "c": 0, "b": 0}}
        print(result)
        if result is not None and result2 is not None:
            userInfo = json.loads(result)
            print("UserInfo")
            print(userInfo)
            random_follower, n = await get_random_updated_follower(user, userInfo, ownInfo)
            if random_follower is not None:
                print("Vai pedir a timeline")
                ask_for_timeline(random_follower[0], random_follower[1], user['id'], n)
                update_vector_clock(n, user['id'], vector_clock)
                
            


# temos de implementar o XOR
async def get_random_updated_follower(user, userInfo, ownInfo):
    try:
        print("user no array following")
        print(user)
        print(userInfo['vector_clock'])  #do a
        print(vector_clock) # o meu
        id=user['id']
        print("id")
        print(id)
        if userInfo['vector_clock'][id] > vector_clock[id] and async_tasks.isOnline(user['ip'], user['port']):
            print("Nao tá atualizado")
            return [user['ip'], user['port']], int(userInfo['vector_clock'][id]) - vector_clock[id] 
        else:
            print("Esta atualizado")
            return None, 0
    except Exception as er:
        print(er)
        print("Esta atualizado")
        return None, 0

# send a message to a node asking for a specific timeline
def ask_for_timeline(userIp, userPort, TLUser, n):
    print("############ask_for_timeline##############")
    msg = builder.timeline_msg(TLUser, vector_clock, n)
    async_tasks.send_p2p_msg(userIp, int(userPort), msg, timeline)

async def ver_tabela(username, server):
    result = await server.get(username)
    print("     TABELA:")
    print(result);


# python peer.py -pDHT 5000 -pP2P 5001
""" MAIN """
if __name__ == "__main__":
    try:
        check_argv()
        args = parse_arguments()
        # configuraçao
        p2p_port = args.pP2P
        DHT_port = args.pDHT
        ipB = args.ipB
        pB = args.pB
        ip_address = get_ip_address()
        
        # inicia o nodo e tenta entrar na rede
        # comunicando-se ao nodo bootstrap
        server = Server()
        loop = asyncio.get_event_loop()
        loop.set_debug(True)
        loop.run_until_complete(server.listen(DHT_port))
        bootstrap_node = (ipB, int(pB))
        loop.run_until_complete(server.bootstrap([bootstrap_node])) 

        print("Entrou na Rede !!!!")

        print('Peer is running...')
        username = get_username()
        
        (timeline, following, vector_clock) = storage.read_data(db_file+username)

        loop.run_until_complete(build_user_info(username))
        
        # bind da ligação TCP
        # para enviar sms e receber timelines atraves da porta tcp
        connection = Connection(ip_address, int(p2p_port))
        # para estar à escuta no socket tcp
        thread = Thread(target = start_p2p_listenner, args = (connection, ))
        thread.start()

        # loop.add_reader(fd, callback, *args)
        # lê do teclado
        loop.add_reader(sys.stdin, handle_stdin)
        
        #asyncio.run(get_timeline())

        loop.run_until_complete(get_timeline())

        m = Menu("Timeline")
        m.draw()
        running = True
        while running:
            print("vetor_clock")
            print(vector_clock)
            print("following")
            print(following)
            msg = loop.run_until_complete(queue.get())
            if msg == "2\n":
                loop.run_until_complete(follow_user())
            else: 
                if msg == "1\n":
                    loop.run_until_complete(show_timeline())
                else:
                    if msg == "3\n":
                        loop.run_until_complete(send_msg())
                        print("send_msg Correu bem")
                    else:
                        if msg == "4\n":
                            loop.run_until_complete(ver_tabela(username, server))
                            print("ver tabela")
                        else:
                            running = False
                #break
            m.draw()

        #loop.run_forever()
        print("ACABOU")
    except Exception as ex:
        print(ex)
    finally:
        print('Good Bye!')
        storage.save_data(timeline, following, vector_clock, db_file+username)        # TODO rm username
        connection.stop()                                                                      # stop thread in "listen mode"
        server.stop()                                                                       # Stop the server with DHT Kademlia
        loop.close()                                                                        # Stop the async loop
        sys.exit(1) 