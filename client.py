import socket
import sys
import selectors
import types
def main():

    start_conn(host, port)

    # checking nick_name duplicate 
    try:
        while True:
            events = sel.select(timeout=1)
            if events:
                for selkey, mask in events:
                    sock = selkey.fileobj
                    data = selkey.data
                    if data.conn is False:
                        set_name(selkey,mask)
                    else:
                        service_conn(selkey, mask)
            if not sel.get_map(): # What is the usage of get_map()
                break
    except KeyboardInterrupt:
        print('keyboard interrput, exiting!')
    finally:
        sel.close()
        

def set_name(key, mask):
    sock = key.fileobj
    data = key.data

    # TODO mulitiple clients and messages queue issues here
    if mask & selectors.EVENT_READ:
        try:
            recv_data = sock.recv(1024)
            if recv_data == b"Accepted":
                print('Received from server: ', repr(recv_data), " your connection ", data.nick_name,"Let's chatting!")
                data.conn = True
        except ConnectionError:
            print('Lost connection!')
            sel.unregister(sock)
            sock.close()
            start_conn(host,port)
        

    if mask & selectors.EVENT_WRITE:
        if not data.nick_name:
            nick_name = input('Set a nickname: ')
            data.nick_name = bytes(nick_name,'utf-8')
            sock.sendall(data.nick_name)
    

def start_conn(host, port):
    """
    Used for building three times hand-shake connection
    """
    server_addr = (host, port)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setblocking(False)
    sock.connect_ex(server_addr)
    events = selectors.EVENT_READ|selectors.EVENT_WRITE

    data = types.SimpleNamespace(nick_name=b'', conn=False)
    sel.register(sock, events, data=data) 

    #print("Received " , repr(data)) # repr() a function used to transfer a object to a string

def service_conn(key, mask):
    # TODO 
    pass

        



if __name__=='__main__':
    """
    host: 127.0.0.1
    port: 7324
    """
    host, port = '127.0.0.1', 7324

    sel = selectors.DefaultSelector()
    kb_nick_name = None
    main()

    