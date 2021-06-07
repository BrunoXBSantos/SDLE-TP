import json
from TCP.Connection import Connection
import builder
import utils
from Functionalities import UtilsFuncionalities

# get timeline to the followings TODO
async def get_timeline(server, username, following, vector_clock, timeline):
    print("################## get_timeline #################")
    for user in following:
        #estou no c, o 'c' segue o 'a' e o 'b'
        # following: [{'id': 'a', 'ip': '192.168.1.82', 'port': 5001}, {'id': 'b', 'ip': '192.168.1.82', 'port': 6001}]
        # user: {'id': 'a', 'ip': '192.168.1.82', 'port': 5001}
        result = await server.get(user['id']) # obtenho o json do 'a', para ver o seu vetor clock
        print("result")
        # {"ip": "192.168.1.82", "port": 5001, "followers": {"c": "192.168.1.82 7001", "b": "192.168.1.82 6001"}, "vector_clock": {"a": 2, "c": 0, "b": 0}}
        print(result)
        if result is not None:
            userDHT = json.loads(result)
            print("UserInfo")
            print(userDHT)
            connection, dif_clock = await check_causality(user, userDHT, vector_clock)
            if connection is not None:
                print("Vai pedir a timeline")
                ask_for_timeline(connection[0], connection[1], user['id'], dif_clock, vector_clock, timeline)
                utils.update_vector_clock(dif_clock, user['id'], vector_clock)
                
            

\
async def check_causality(user, userDHT, vector_clock):
    try:
        print("user no array following")
        print(user)
        print(userDHT['vector_clock'])  #do a
        print(vector_clock) # o meu
        id=user['id']
        print("id")
        print(id)
        if userDHT['vector_clock'][id] > vector_clock[id] and UtilsFuncionalities.isOnline(user['ip'], user['port']):
            print("Nao tá atualizado")
            return [user['ip'], user['port']], int(userDHT['vector_clock'][id]) - vector_clock[id] 
        else:
            print("Esta atualizado")
            return None, 0
    except Exception as er:
        print(er)
        print("Esta atualizado")
        return None, 0

# send a message to a node asking for a specific timeline
def ask_for_timeline(userIp, userPort, TLUser, dif_clock, vector_clock, timeline):
    print("############ask_for_timeline##############")
    msg = builder.timeline_msg(TLUser, vector_clock, dif_clock)
    UtilsFuncionalities.send_p2p_msg(userIp, int(userPort), msg, timeline)
