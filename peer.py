import argparse
import asyncio
import sys
from kademlia.network import Server
from threading import Thread
from TCP.Connection import Connection
import utils
import builder
from Menu.Menu import Menu
import Menu.Menu as menu
from Storage import storage

from Funcionalities import FollowUser
from Funcionalities import GetTimeline
from Funcionalities import ShowTimeline
from Funcionalities import PostMessage



# -- Global VARS --
queue = asyncio.Queue()
p2p_port = ""
username = ""
ip_address = ""
timeline = []
following = []
vector_clock = {}
db_file = 'db'

# exit app
def exit_loop():
    return True

# check if the number of args is valid
def check_argv():
    if len(sys.argv) < 3:
        print("Usage: python peer.py <-pDHT port_dht> <-pP2P port_p2p> [<-ipB bootstrap_ip> <-pB bootstrap_port>]")
        sys.exit(1)

# put the peer in "Listen mode" for new connections
def start_p2p_listenner(connection):
    print("########### start_p2p_listenner ##########")
    connection.bind()
    connection.listen(timeline, server, username, vector_clock)

# handler process IO request
def handle_stdin():
    data = sys.stdin.readline()
    asyncio.ensure_future(queue.put(data)) # Queue.put is a coroutine, so you can't call it directly.


def parse_arguments():
    parser = argparse.ArgumentParser()
    # Optional arguments
    parser.add_argument("-ipB", "--ipB", help="IP address of Bootstrap node", type=str, default="0.0.0.0")
    parser.add_argument("-pB", "--pB", help="port number of Bootstrap node", type=int, default=2000)
    parser.add_argument("-pDHT", "--pDHT", help="UDP port", type=int, default=None)
    parser.add_argument("-pP2P", "--pP2P", help="TCP port", type=int, default=None)
    return parser.parse_args()

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
        ip_address = utils.get_ip_address()
        
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
        username = utils.get_username()
        
        (timeline, following, vector_clock) = storage.read_data(db_file+username)

        loop.run_until_complete(builder.build_user_info(username, server, ip_address, p2p_port, vector_clock))
        
        # bind da ligação TCP
        # para enviar sms e receber timelines atraves da porta tcp
        connection = Connection(ip_address, int(p2p_port))
        # para estar à escuta no socket tcp
        thread = Thread(target = start_p2p_listenner, args = (connection, ))
        thread.start()

        # loop.add_reader(fd, callback, *args)
        # lê do teclado
        loop.add_reader(sys.stdin, handle_stdin)
        
        loop.run_until_complete(GetTimeline.get_timeline(server, username, following, vector_clock, timeline))

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
                loop.run_until_complete(FollowUser.follow_user(username, following, server, ip_address, p2p_port))
            else: 
                if msg == "1\n":
                    loop.run_until_complete(ShowTimeline.show_timeline(menu, timeline))
                else:
                    if msg == "3\n":
                        loop.run_until_complete(PostMessage.post_msg(timeline, username, server, vector_clock))
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