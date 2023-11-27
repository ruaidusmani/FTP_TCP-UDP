import socket

HOST = "localhost"
PORT = 12000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as Server_Socket:
    Server_Socket.bind((HOST,PORT))
    Server_Socket.listen(0)

    print ("Server is waiting for client connection")
    conn,addr = Server_Socket.accept()
    
    with conn:
        print("Connected by", addr)
        print("Success")
