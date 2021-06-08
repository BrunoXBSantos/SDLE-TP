import json
from TCP.Connection import Connection
import builder
import utils
from Functionalities import UtilsFuncionalities

# get timeline to the subscribeds TODO
async def get_timeline(server, username, subscribed, vector_clock, timeline):
    for user in subscribed:
        #estou no c, o 'c' segue o 'a' e o 'b'
        # subscribed: [{'id': 'a', 'ip': '192.168.1.82', 'port': 5001}, {'id': 'b', 'ip': '192.168.1.82', 'port': 6001}]
        # user: {'id': 'a', 'ip': '192.168.1.82', 'port': 5001}
        result = await server.get(user['id']) # obtenho o json do 'a', para ver o seu vetor clock
        # {"ip": "192.168.1.82", "port": 5001, "subscribers": {"c": "192.168.1.82 7001", "b": "192.168.1.82 6001"}, "vector_clock": {"a": 2, "c": 0, "b": 0}}
        print(result)
        if result is not None:
            userDHT = json.loads(result)
            connection, dif_clock = await check_causality(user, userDHT, vector_clock)
            if connection is not None:
                ask_for_timeline(connection[0], connection[1], user['id'], dif_clock, vector_clock, timeline)
                utils.update_vector_clock(dif_clock, user['id'], vector_clock)
                
            

\
async def check_causality(user, userDHT, vector_clock):
    try:
        id=user['id']
        if userDHT['vector_clock'][id] > vector_clock[id] and UtilsFuncionalities.isOnline(user['ip'], user['port']):
            return [user['ip'], user['port']], int(userDHT['vector_clock'][id]) - vector_clock[id] 
        else:
            return None, 0
    except Exception as er:
        print(er)
        return None, 0

# send a message to a node asking for a specific timeline
def ask_for_timeline(userIp, userPort, TLUser, dif_clock, vector_clock, timeline):
    msg = builder.GetTimeline(TLUser, vector_clock, dif_clock)
    UtilsFuncionalities.send_p2p_msg(userIp, int(userPort), msg, timeline)
