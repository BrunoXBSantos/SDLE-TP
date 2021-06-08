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
from datetime import datetime

from Functionalities import SubscribeUsername
from Functionalities import GetTimeline
from Functionalities import SeeTimeline
from Functionalities import PostMessage
from Functionalities import GetSubscribers



# -- Global VARIABLES --
queue = asyncio.Queue()
p2p_port = ""
username = ""
ip_address = ""
timeline = []
subscribed = []
vector_clock = {}
storage_file = 'database_'

# exit app
def exit_loop():
    return True

# check if the number of args is valid
def verify_args():
    if len(sys.argv) < 3:
        print("Usage: python peer.py <-pDHT port_dht> <-pP2P port_p2p> [<-ipB bootstrap_ip> <-pB bootstrap_port>]")
        sys.exit(1)

# thread that listens for messages
def thread_listener(connection):
    connection.bind()
    connection.listen(timeline, server, username, vector_clock)

# thread that asynchronously waits for the keyboard
def handle_stdin():
    data = sys.stdin.readline()
    asyncio.ensure_future(queue.put(data))


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
if __name__ == "__main__":
    try:
        verify_args()
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

        print('Peer is active ...')
        username = utils.get_username()
        
        (timeline, subscribed, vector_clock) = storage.read_data(storage_file+username)

        loop.run_until_complete(builder.build_user_info(username, server, ip_address, p2p_port, vector_clock))
        
        # bind da ligação TCP
        # para enviar sms e receber timelines atraves da porta tcp
        connection = Connection(ip_address, int(p2p_port))
        # para estar à escuta no socket tcp
        thread = Thread(target = thread_listener, args = (connection, ))
        thread.start()

        # lê do teclado
        loop.add_reader(sys.stdin, handle_stdin)
        
        loop.run_until_complete(GetTimeline.get_timeline(server, username, subscribed, vector_clock, timeline))

        m = Menu("   Welcome  " + datetime.now().strftime('%d/%m/%Y %H:%M'))
        m.draw()
        running = True
        while running:
            msg = loop.run_until_complete(queue.get())
            if msg == "2\n":
                loop.run_until_complete(SubscribeUsername.subscribe_username(username, subscribed, server, ip_address, p2p_port, vector_clock[username]))
                menu.clear_screen()
            else: 
                if msg == "1\n":
                    loop.run_until_complete(SeeTimeline.see_timeline(menu, timeline))
                    menu.clear_screen()
                else:
                    if msg == "3\n":
                        loop.run_until_complete(PostMessage.post_msg(timeline, username, server, vector_clock))
                        menu.clear_screen()
                    else:
                        if msg == "4\n":
                            loop.run_until_complete(GetSubscribers.getSubscribers(server, username, menu))
                            menu.clear_screen()
                        else:
                            if msg == "5\n":
                                loop.run_until_complete(ver_tabela(username, server))
                                print("ver tabela")
                            else:
                                running = False
            #menu.clear_screen()
            m.draw()

        #loop.run_forever()
        print("Programa terminado com sucesso!")
        sys.exit(1) 
    except Exception as ex:
        print(ex)
    finally:
        print('Good Bye!')
        storage.save_data(timeline, subscribed, vector_clock, storage_file+username)        
        connection.stop()                                                                      
        server.stop()                                                                       
        loop.close()                                                                        
        sys.exit(1) 