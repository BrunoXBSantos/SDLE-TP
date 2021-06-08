import asyncio
import json
import asyncio, json

# follow a user. After, he can be found in the list "subscribed"
async def subscribe_username(username, subscribed, server, ip_address, p2p_port, value_clock):
    user = input('Subscribe username: ')
    user_id = user.replace('\n', '')
    result = await server.get(user_id)
    if result is None:
        print('Username does not exist!')
    else:
        userInfo = json.loads(result)
        print(userInfo)
        try:
            if userInfo['subscribers'][username]:
                print('You are subscribed him!')

        except Exception as err:
            subscribed.append({'id': user_id, 'ip': userInfo['ip'], 'port': userInfo['port']})
            userInfo['subscribers'][username] = f'{ip_address} {p2p_port}'
            userInfo['vector_clock'][username] = value_clock
            asyncio.ensure_future(server.set(user_id, json.dumps(userInfo)))
            return True
    return True