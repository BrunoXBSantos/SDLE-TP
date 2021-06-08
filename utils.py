import socket

def update_vector_clock(n, id, vector_clock):
    try:
        vector_clock[id] += n
        print("vetor_clock " )
        print(vector_clock)
    except Exception:
        vector_clock[id] = n
        print("vetor_clock " )
        print(vector_clock)

# get username
def get_username():
    nick = input('username: ')
    return nick.replace('\n', '')

# Get ip
def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip