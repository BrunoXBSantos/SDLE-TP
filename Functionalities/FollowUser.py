import asyncio
import json
import asyncio, json

# follow a user. After, he can be found in the list "following"
async def subscribe_username(username, following, server, ip_address, p2p_port, value_clock):
    user = input('Subscribe username: ')
    user_id = user.replace('\n', '')
    result = await server.get(user_id)
    if result is None:
        print('Username does not exist!')
    else:
        userInfo = json.loads(result)
        print(userInfo)
        try:
            if userInfo['followers'][username]:
                print('You are following him!')

        except Exception as err:
            following.append({'id': user_id, 'ip': userInfo['ip'], 'port': userInfo['port']})
            userInfo['followers'][username] = f'{ip_address} {p2p_port}'
            userInfo['vector_clock'][username] = value_clock
            asyncio.ensure_future(server.set(user_id, json.dumps(userInfo)))
            print(await (server.get(user_id)))
            return True
    return True