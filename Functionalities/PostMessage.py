import asyncio
import json
import builder
import asyncio, json
from Functionalities import UtilsFuncionalities


# send message to the subscribers
async def post_msg(timeline, username, server, vetor_clock):
    msg = input('Insert message: ')
    msg = msg.replace('\n','')
    timeline.append({'id': username, 'message': msg})
    result = builder.simple_msg(msg, username)
    await (task_send_msg(result, server, username, vetor_clock))
    return False

    # get subscribers port's
# vai colocando no array connection_info os seguidores
async def get_subscribers(server, username, vector_clock):
    connection_info = []
    result = await server.get(username)
    if result is None:
        print('ERROR - Why don\'t I belong to the DHT?')
    else:
        userInfo = json.loads(result)
        userInfo['vector_clock'][username] += 1
        vector_clock[username] += 1
        await (server.set(username, json.dumps(userInfo)))
        for user, info in userInfo['subscribers'].items():
            connection_info.append(info)
    return connection_info


async def task_send_msg(msg, server, username, vector_clock):
    connection_info = await get_subscribers(server, username, vector_clock)
    for subscribe in connection_info:
        info = subscribe.split()
        UtilsFuncionalities.send_p2p_msg(info[0], int(info[1]), msg, vector_clock)





