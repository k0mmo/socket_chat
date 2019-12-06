import socket

HOST = ''
PORT = 4040

def create_listen_socket(host, port):
    # Sets up sockets the server will receive
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # uses ipv4 and tcip
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port)) # binds socket to host ip and port
    sock.listen(100) # listens for up to 100 ques
    return sock

def prep_msg(msg):
    # preps string to be sent as a msg
    msg += '\0'
    return msg.encode('utf-8')

def send_msg(sock, msg):
    # sends a string over a socket going threw prep 1st
    data = prep_msg(msg)
    sock.sendall(data)

def parse_recvd_data(data):
    """ Break up raw received data into messages, delimited
        by null byte """
    parts = data.split(b'\0')
    msgs = parts[:-1]
    rest = parts[-1]
    return (msgs, rest)

def recv_msgs(sock, data=bytes()):
    """ Receive data and break into complete messages on null byte
        delimiter. Block until at least one message received, then
        return received messages """
    msgs = []
    while not msgs:
        recvd = sock.recv(4096)
        if not recvd:
            raise ConnectionError()
        data = data + recvd
        (msgs, rest) = parse_recvd_data(data)
    msgs = [msg.decode('utf-8') for msg in msgs]
    return (msgs, rest)
