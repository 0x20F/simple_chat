import socket
from threading import Thread



# Always running, ready to welcome anyone that wants to connect
def a_conn():
    while True:
        # Accept the connection
        c, c_address = sv.accept()

        # Server-side message
        print("[i] %s:%s has connected." % c_address)
        
        addresses[c] = c_address
        # Build them a thread and await the response there
        Thread(target=c_handle, args=(c,)).start()




# Every client gets a thread with this, this thread
# listens for things they will eventually say and then
# sends it out to everyone
def c_handle(client):    
    
    # Check wether or not the user should actually connect here
    auth = client.recv(BUFF_SIZE).decode("utf8")
    print("[~] Client auth token is: %s " % auth)
    
    # Stupid auth...
    if auth == "r muffins cakes?":
        client.send(bytes("muffins r cakes", "utf8"))
    else:
        # If you don't have the right key, buh bye
        client.send(bytes("[!] Auth failed!", "utf8"))
        client.close()
        return

    # Welcome the user
    client.send(bytes("[+] Welcome to shitshow!\n[~] Now type your name and press enter!", "utf8"))
    name = client.recv(BUFF_SIZE).decode("utf8")

    # Prepare messages with that name
    welcome_msg = '[i] Welcome, %s! You can exit the game/chat by typing !exit' % name
    join_msg = "[~] %s has connected!" % name
    
    # Send the client a welcome message and 
    # add him/her to the list of connected clients
    client.send(bytes(welcome_msg, "utf8"))
    clients[client] = name

    # Tell everyone, apart from this client, that someone has connected
    bcast(msg=bytes(join_msg, "utf8"), exc=client)

    # Start an endless loop so the above code
    # doesn't have to run more than once.
    while True:
        # Keep checking if the client says something
        try:
            msg = client.recv(BUFF_SIZE)
        
            if msg != bytes("/quit/", "utf8"):
                bcast(msg, name+": ", client)
            else:
                client.send(bytes("/quit/", "utf8"))
                client.close()
                del clients[client]
                
                bcast(bytes("[~] %s has left the chat." % name, "utf8"))
                break
        except:
            # Client has disconnected
            print("[i] %s:%s/%s has disconnected!" % (addresses[client][0], addresses[client][1], name))
            
            client.close()
            del clients[client]
            
            bcast(bytes("[~] %s has left the chat." % name, "utf8"))
            return




# Used to broadcast messages from one user to everyone
def bcast(msg, prefix="", exc=None):
    # For every client, send them the message...
    for s in clients:
        # ...unless that client is you, you don't want your own message
        if s == exc:
            continue

        s.send(bytes(prefix, "utf8") + msg)

        
clients = {}
addresses = {}

HOST = ''
PORT = 33000
BUFF_SIZE = 4096
ADDR = (HOST, PORT)

sv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sv.bind(ADDR)


# 200 connections max for now, increase if necessary
sv.listen(200)
print("[i] Awaiting connection...")

ACCEPT_THREAD = Thread(target=a_conn)
ACCEPT_THREAD.start()
ACCEPT_THREAD.join()

sv.close()