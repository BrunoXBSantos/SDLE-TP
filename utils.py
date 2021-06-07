import socket

def update_vector_clock(n, id, vector_clock):
    print('hei')
    try:
        print("vetor_clock " )
        print(vector_clock)
        vector_clock[id] += n
        print("vetor_clock " )
        print(vector_clock)
    except Exception:
        vector_clock[id] = n
        print("vetor_clock " )
        print(vector_clock)

# get the username
def get_username():
    nick = input('username: ')
    return nick.replace('\n', '')

# Get user real ip
def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip