import json

# value stored in DHT
def user_info(username, ip_address, p2p_port):
    info = {'ip': ip_address, 'port': p2p_port, 'subscribers': {}, 'vector_clock': {username: 0}}
    return json.dumps(info)


# Timeline submission
def simple_msg(msg, username):
    simple_msg = {'type': 'simple', 'msg': msg, 'id': username}
    return json.dumps(simple_msg)


# timeline request
def GetTimeline(id, vclock, n):
    timeline_msg = {'type': 'timeline', 'id': id, 'v_clock': vclock, 'n': n}
    return json.dumps(timeline_msg) 

# build a json with user info and put it in the DHT
async def build_user_info(username, server, ip_address, p2p_port, vector_clock):
    exists = await server.get(username)
    print(exists)    #check if user exists in DHT
    if exists is None:
        info = user_info(username, ip_address, p2p_port)
        vector_clock[username] = 0
        await (server.set(username, info))