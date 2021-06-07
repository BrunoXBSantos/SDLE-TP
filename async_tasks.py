import asyncio, json, socket
from asyncio.events import get_event_loop
from asyncio.tasks import sleep
from builder import user_info
from P2P.Connection import Connection

# process all messages into the Queue
@asyncio.coroutine
def task(server, loop, nickname, menu, queue):
    menu.draw()
    while True:
        msg = yield from queue.get()
        print("dadawdawdawd " + msg)
        if not msg == '\n' and menu.run(int(msg)):
            break
        menu.draw()
    loop.call_soon_threadsafe(loop.stop)


async def task_follow(user_id, nickname, server, following, ip_address, p2p_port, vector_clock):
    result = await server.get(user_id)

    if result is None:
        print('That user doesn\'t exist!')
    else:
        userInfo = json.loads(result)
        print(userInfo)
        try:
            if userInfo['followers'][nickname]:
                print('You\'re following him!')
        except Exception:
            print('Following ' + user_id)
            following.append({'id': user_id, 'ip': userInfo['ip'], 'port': userInfo['port']})
            userInfo['followers'][nickname] = f'{ip_address} {p2p_port}'
            userInfo['vector_clock'][nickname] = 0
            print("SETTTTTTTTTTTTT")
            await (server.set(user_id, json.dumps(userInfo)))
            print("GETTTTTTTTTTTTT")
            print(await (server.get(user_id)))
            print("DEUUUUUUUUUUUU")



# get followers port's
# vai colocando no array connection_info os seguidores
async def get_followers_p2p(server, nickname, vector_clock):
    print("######### get_followers_p2p #########")
    connection_info = []
    result = await server.get(nickname)
    if result is None:
        print('ERROR - Why don\'t I belong to the DHT?')
    else:
        userInfo = json.loads(result)
        userInfo['vector_clock'][nickname] += 1
        vector_clock[nickname] += 1
        print(userInfo)
        asyncio.ensure_future (server.set(nickname, json.dumps(userInfo)))
        print("AAAAAAAAAAAAAAAAAAAAAAAAA")
        for user, info in userInfo['followers'].items():
            connection_info.append(info)
    return connection_info


async def task_send_msg(msg, server, nickname, vector_clock):
    print("######### task_send_msg #########")
    connection_info = await get_followers_p2p(server, nickname, vector_clock)
    print("######### task_send_msg #########")
    print(connection_info)
    print('CONNECTION INFO (Ip, Port)')
    for follower in connection_info:
        print(follower)
        info = follower.split()
        send_p2p_msg(info[0], int(info[1]), msg, vector_clock)


def send_p2p_msg(ip, port, message, timeline=None):
    print("######### send_p2p_msg #########")
    if isOnline(ip, port):
        connection = Connection(ip, port)
        connection.connect()
        connection.send(message, timeline)
        print("Enviado")
        print("SEND MESSAGE c'est FINI")


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
