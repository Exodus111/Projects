#!/usr/bin/python3
# Simple Python3 example of connecting to a host
# using a Socket.
from socket import socket, gethostbyname, AF_INET, SOCK_STREAM

URL = "www.google.com"
PORT = 80
MESSAGE = "GET / HTTP/1.1\r\n\r\n"

s = socket(AF_INET, SOCK_STREAM)
remote_ip = gethostbyname(URL)
s.connect((remote_ip, PORT))
s.sendall(MESSAGE.encode())
reply = s.recv(4096)

print(reply)

