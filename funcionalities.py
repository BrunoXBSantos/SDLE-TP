# get the nickname
def get_nickname():
    nick = input('Nickname: ')
    return nick.replace('\n', '')


# follow a user. After, he can be found in the list "following"
def follow_user():
    user = input('User Nickname: ')
    user_id = user.replace('\n', '')
    loop.run_until_complete(async_tasks.task_follow(user_id, nickname, server, following, ip_address, p2p_port, vector_clock))
    return False


# show own timeline
def show_timeline():
    menu.clear()
    print('_______________ Timeline _______________')
    for m in timeline:
        print(m['id'] + ' - ' + m['message'])
    print('________________________________________')
    input('Press Enter')
    menu.clear()
    return False


# send message to the followers
def send_msg():
    msg = input('Insert message: ')
    msg = msg.replace('\n','')
    timeline.append({'id': nickname, 'message': msg})
    print(msg)
    result = builder.simple_msg(msg, nickname)
    loop.run_until_complete(async_tasks.task_send_msg(result, server, nickname, vector_clock))

    return False


# exit app
def exit_loop():
    return True