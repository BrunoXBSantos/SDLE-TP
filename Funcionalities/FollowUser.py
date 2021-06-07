import asyncio
import json
import asyncio, json

# follow a user. After, he can be found in the list "following"
async def follow_user(username, following, server, ip_address, p2p_port):
    user = input('User username: ')
    user_id = user.replace('\n', '')
    
    result = await server.get(user_id)

    if result is None:
        print('That user doesn\'t exist!')
    else:
        userInfo = json.loads(result)
        print(userInfo)
        try:
            if userInfo['followers'][username]:
                print('You\'re following him!')

        except Exception as err:
            following.append({'id': user_id, 'ip': userInfo['ip'], 'port': userInfo['port']})
            userInfo['followers'][username] = f'{ip_address} {p2p_port}'
            userInfo['vector_clock'][username] = 0
            asyncio.ensure_future(server.set(user_id, json.dumps(userInfo)))
            print(await (server.get(user_id)))
            return True
    return True