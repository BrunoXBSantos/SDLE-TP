import argparse
import asyncio
from asyncio.runners import run
import json
import random
import sys, socket

from threading import Thread
from P2P.Connection import Connection
import builder
from Menu.Menu import Menu
import Menu.Menu as menu
from Menu.Item import Item
import async_tasks
from LocalStorage import local_storage

from kademlia.network import Server


# -- Global VARS --
queue = asyncio.Queue()
p2p_port = ""
nickname = ""
ip_address = ""
timeline = []
following = []
vector_clock = {}
db_file = 'db'


# get the nickname
def get_nickname():
    nick = input('Nickname: ')
    return nick.replace('\n', '')


# follow a user. After, he can be found in the list "following"
async def follow_user():
    user = input('User Nickname: ')
    user_id = user.replace('\n', '')
    
    result = await server.get(user_id)

    if result is None:
        print('That user doesn\'t exist!')
    else:
        userInfo = json.loads(result)
        print(userInfo)
        try:
            if userInfo['followers'][nickname]:
                print('You\'re following him!')

        except Exception as err:
            print("EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE")
            print(err)
            print("EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE")
            print('Following ' + user_id)
            following.append({'id': user_id, 'ip': userInfo['ip'], 'port': userInfo['port']})
            userInfo['followers'][nickname] = f'{ip_address} {p2p_port}'
            userInfo['vector_clock'][nickname] = 0
            print("SETTTTTTTTTTTTT")
            asyncio.ensure_future(server.set(user_id, json.dumps(userInfo)))
            print("GETTTTTTTTTTTTT")
            print(await (server.get(user_id)))
            print("DEUUUUUUUUUUUU")
            return True
    return True


# show own timeline
async def show_timeline():
    menu.clear()
    print('_______________ Timeline _______________')
    for m in timeline:
        print(m['id'] + ' - ' + m['message'])
    print('________________________________________')
    input('Press Enter')
    menu.clear()
    return False


# send message to the followers
async def send_msg():
    print("######### send_msg #########")
    msg = input('Insert message: ')
    msg = msg.replace('\n','')
    timeline.append({'id': nickname, 'message': msg})
    print(msg)
    result = builder.simple_msg(msg, nickname)
    await (async_tasks.task_send_msg(result, server, nickname, vector_clock))
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


# get the nickname
def get_nickname():
    nick = input('Nickname: ')
    return nick.replace('\n', '')

# put the peer in "Listen mode" for new connections
def start_p2p_listenner(connection):
    print("########### start_p2p_listenner ##########")
    connection.bind()
    connection.listen(timeline, server, nickname, vector_clock)

# handler process IO request
def handle_stdin():
    data = sys.stdin.readline()
    asyncio.ensure_future(queue.put(data)) # Queue.put is a coroutine, so you can't call it directly.


# build a json with user info and put it in the DHT
async def build_user_info(nickname):
    exists = await server.get(nickname)
    print(exists)    #check if user exists in DHT
    if exists is None:
        info = builder.user_info(nickname, ip_address, p2p_port)
        vector_clock[nickname] = 0
        await (server.set(nickname, info))
        print("Inserido na DHT crlh!!!!!!!!!!!")
        ##print("Nao existe crlh")
        ##await server.set(nickname, 1)
        ##print(await server.get(nickname))


# build the Menu
def build_menu():
    menu = Menu('Menu')
    menu.add_item(Item('1 - Show timeline', show_timeline))
    menu.add_item(Item('2 - Subscribe username', (follow_user)))
    menu.add_item(Item('3 - Send message', send_msg))
    menu.add_item(Item('0 - Exit', exit_loop))
    return menu

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
    for user in following:
        result = await server.get(user['id'])
        result2 = await server.get(nickname)
        if result is not None and result2 is not None:
            userInfo = json.loads(result)
            ownInfo = json.loads(result2)
            random_follower, n = await get_random_updated_follower(user, userInfo, ownInfo)
            if random_follower is not None:
                ask_for_timeline(random_follower[0], random_follower[1], user['id'], n)
            


# temos de implementar o XOR
async def get_random_updated_follower(user, userInfo, ownInfo):
    print("RANDOM FOLLOWER")
    id = user['id']
    user_followers = userInfo['followers']
    while(user_followers):
        random_follower = random.choice(list(user_followers.keys()))
        random_follower_con = userInfo['followers'][random_follower]
        info = random_follower_con.split()
        print(userInfo['vector_clock'])
        print(vector_clock)
        if userInfo['vector_clock'][id] > vector_clock[id] and random_follower != nickname and async_tasks.isOnline(info[0], int(info[1])):
        #if random_follower != nickname and async_tasks.isOnline(info[0], int(info[1])):
            print("FOUND")
            return info, int(userInfo['vector_clock'][id]) - vector_clock[id] 
        user_followers.pop(random_follower)
    print("FAILED")
    if userInfo['vector_clock'][id] > vector_clock[id]:
        return [user['ip'], user['port']], int(userInfo['vector_clock'][id]) - vector_clock[id] 
    else:
        return None, 0

# send a message to a node asking for a specific timeline
def ask_for_timeline(userIp, userPort, TLUser, n):
    msg = builder.timeline_msg(TLUser, vector_clock, n)
    async_tasks.send_p2p_msg(userIp, int(userPort), msg, timeline)
    print('ASKING FOR TIMELINE')


# merge all timelines TODO
def merge_timelines():
    print('TODO')


# check a set of vector clocks TODO
def check_vector_clocks():
    print('TODO')     


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
        nickname = get_nickname()
        
        #(timeline, following, vector_clock) = local_storage.read_data(db_file+nickname)
        
        print("Timeline: ") 
        print(timeline)
        print("following: ")
        print(following)
        print("vector_clock: ")
        print(vector_clock)


        loop.run_until_complete(build_user_info(nickname))
        
        #(  , following, vector_clock) = local_storage.read_data(db_file+nickname)     # TODO rm nickname (it's necessary for to allow tests in the same host

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
    
        m = build_menu()
        m.draw()
        running = True
        while running:
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
                        running = False
                #break
            m.draw()

        #loop.run_forever()
        print("ACABOU")
    except Exception as ex:
        print(ex)
    finally:
        print('Good Bye!')
        local_storage.save_data(timeline, following, vector_clock, db_file+nickname)        # TODO rm nickname
        connection.stop()                                                                      # stop thread in "listen mode"
        server.stop()                                                                       # Stop the server with DHT Kademlia
        loop.close()                                                                        # Stop the async loop
        sys.exit(1) 