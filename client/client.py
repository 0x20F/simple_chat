import socket
import os, sys
import netscan
import getpass
from threading import Thread


chat = ""
user_input = ""

# Keep listening for messages
def receive():
    global chat

    while 1:
        try:
            msg = cs.recv(BUFF_SIZE).decode("utf8")
            chat += msg + "\n"
            netscan.clear()
            print(chat)
        except:
            print("[i] Server connection lost!")
            break




BUFF_SIZE = 4096

name = ""
cs = netscan.find_host()
r_thread = Thread(target=receive).start()

while 1:
    msg = input()

    # Ugly but it works I guess
    # Will only run the first time
    # someone types something in and
    # that's the name.
    if len(name) < 1:
        name = msg


    if msg == "clean": 
        netscan.clear()
        continue

    elif msg == "!exit": 
        cs.close()
        print("[i] Disconnected.")
        sys.exit()

    chat += name + ": " + msg + "\n"
    netscan.clear()
    print(chat)

    cs.send(bytes(msg, "utf8"))