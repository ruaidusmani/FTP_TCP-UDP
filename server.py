import socket
import threading

HOST = "127.0.0.1" #localhost
PORT = 12000 # listening port

def handle_tcp_client(client, addr):
    print("Connected by TCP at ", addr)
    print("Success")

    while True:
        data = client.recv(1024).decode()
        if not data:
            break

        if data == "bye":
            break
        
        opcode = opcode = data[:3]
        file_length_binary = data[3:8]
        file_name_binary = data[8:]

        file_length = int(file_length_binary, 2)
        # Decode file name binary to retrieve the file name
        file_name = ''.join(chr(int(file_name_binary[i:i+8], 2)) for i in range(0, len(file_name_binary), 8))

        # Perform actions based on the parsed command
        # Example: Print the parsed command details
        print("Received Command from TCP Client:")
        print(f"Opcode: {opcode}")
        print(f"File Length Binary: {file_length_binary}")
        print(f"File Length: {file_length}")
        print(f"File Name: {file_name}")

    client.close()

def tcp_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_socket:
        tcp_socket.bind((HOST,PORT))
        tcp_socket.listen(0)

        print ("Server is waiting for TCP client connection")

        while True:
            client, addr = tcp_socket.accept()
            client_thread = threading.Thread(target=handle_tcp_client, args=(client, addr))
            client_thread.start()

        
        # conn,addr = tcp_socket.accept()
        
        # with conn:
        #     print("Connected by TCP at ", addr)
        #     print("Success")
            

def udp_server():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
        udp_socket.bind((HOST,PORT))
        print("UDP Server is waiting for client connection")
        conn,addr = udp_socket.recvfrom(1024)
        with conn:
            print("Connected by UDP at ", addr)
            print("Success")


tcp_thread = threading.Thread(target=tcp_server)
udp_thread = threading.Thread(target=udp_server)

tcp_thread.start()
udp_thread.start()
