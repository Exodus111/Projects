#!/usr/bin/python3
# Simple Server/Client connection example (Client).
import socket


user = input("Input Your Username: ") 

HOST = "127.0.0.1"
PORT = 5000


s = socket.socket()
s.connect((HOST, PORT))
msg = input("-> ")

while msg != "q":
	message = user + " " + msg
	s.send(message.encode())
	data = s.recv(1024).decode()
	print(data)
	msg = input("-> ")
s.close()