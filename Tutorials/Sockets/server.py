#!/usr/bin/python3
# Simple Server/Client connection example (Server).
import socket

HOST = "127.0.0.1"
PORT = 5000

s = socket.socket()
s.bind((HOST, PORT))
s.listen(2)
connections = []
connections.append(s.accept()[0])

while True:
	for conn in connections:	
		data = conn.recv(1024).decode()
		data = str(data)
		user, *msg = data.split(" ")	
		print("{}: {}".format(user, " ".join(msg)))
		conn.send(data.encode())
[conn.close() for conn in connections]
