import socket
import time
import os, sys
from threading import Thread
from ipaddress import IPv4Network as ipv4


# Check-Variable to see when the thread should stop
loading = True


# Clear the screen in case it looks messy
def clear():
    os.system("cls" if os.name == "nt" else "clear")


# Used to check if a connection can be made to a specific ip
# returns: socket connection to that ip
def is_up(addr):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Set the timeout to 0.01s so this runs fast
    s.settimeout(0.01)      
    
    # Connect to the host on port 33k
    if not s.connect_ex((addr, 33000)):
        # Send the 'magnificent' authentication phrase  
        s.send(bytes("r muffins cakes?", "utf8"))

        # Wait for a response.
        # This might be bad if it was a big worldwide network
        # or something but it's a LAN so things will run
        # fast enough
        while 1:
            # Remove the timeout so we don't DC while waiting for an answer
            s.settimeout(None)
            response = s.recv(1024).decode("utf8")

            # If the response is the phrase we're looking for
            # then it's the right server. This isn't safe since
            # other people could make their own servers with bad
            # stuff and act as this but OH WELL...
            if response == "muffins r cakes":
                return s
            else:
                s.close()
                return
                
    else:
        s.close()


# Used to loop through ip addresses until we can connect to one
# or give up. This needs to exist since the ip of the server is dynamic
# and won't be kept in check, the client will have to scan for 
# a host. Let's call the wait time "matchmaking"...
def find_host():
    # Start the loading "animation" thread
    Thread(target=load).start()

    # Wether or not we're still searching for ip, this is for the 
    # loading "animation"
    global loading

    # 192.168.{i}.0
    for i in range(1, 256):
        for ip in ipv4("192.168.%d.0/24" % i):
            s = is_up(str(ip))
            if s:
                loading = False

                # Return the socket to use for the connection
                return s

    print("[i] There are no hosts online! Exiting.")
    sys.exit()


# The loading "animation"
def load():
    clear()
    dots = ""

    while 1:
        # If loading == False, stop animating
        if not loading: return
        
        # Else, add another dot
        dots += "."

        if dots == "....":
            dots = "."
        
        # Write with a carriage return so the new text can
        # appear on the same line.
        sys.stdout.write("[i] Finding host%s      \r" % dots)
        sys.stdout.flush()

        # Sleep for a second so the animation looks smoother.
        time.sleep(1)
        
