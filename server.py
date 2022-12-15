import socket
import os
HOST='127.0.0.1'
PORT=8080
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((HOST,PORT))
s.listen(5)
while True:
    client,addr=s.accept()
    data=client.recv(1024).decode()
    with open("passwd.txt",'w') as f:
        f.write(data)
    while True:
        pass
