import asyncio, json, socket
from P2P.Connection import Connection

# get followers port's
# vai colocando no array connection_info os seguidores
async def get_followers_p2p(server, username, vector_clock):
    print("######### get_followers_p2p #########")
    connection_info = []
    result = await server.get(username)
    if result is None:
        print('ERROR - Why don\'t I belong to the DHT?')
    else:
        userInfo = json.loads(result)
        userInfo['vector_clock'][username] += 1
        vector_clock[username] += 1
        print(userInfo)
        asyncio.ensure_future (server.set(username, json.dumps(userInfo)))
        print("AAAAAAAAAAAAAAAAAAAAAAAAA")
        for user, info in userInfo['followers'].items():
            connection_info.append(info)
    return connection_info


async def task_send_msg(msg, server, username, vector_clock):
    print("######### task_send_msg #########")
    connection_info = await get_followers_p2p(server, username, vector_clock)
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
