import socket
import threading
import concurrent.futures
import time
import os

HOST = "127.0.0.1" #localhost
PORT = 12000 # listening port

MAX_THREADS = 10

def handle_summary_request(data):
    print("Received summary request from client")

    # Parse the command
    opcode = data[:3] # opcode 
    file_length_binary = data[3:8] # get file length binary
    file_name_binary = data[8:] # get file name binary

    file_length = int(file_length_binary, 2) # convert binary to int for file length
    
    # Decode file name binary to retrieve the file name
    file_name = ''.join(chr(int(file_name_binary[i:i+8], 2)) for i in range(0, len(file_name_binary), 8))

    print ("Parsed file name ", file_name)

    if os.path.exists(file_name): # check if file exists in directory 
        try: 
            with open(file_name, 'r') as file: # Open and read the file content
                file_content = file.read()
                integer_array = [int(i) for i in file_content.split(',')] # store text in array of integers

                # Perform max, min, and average 
                max_val = max(integer_array)
                min_val = min(integer_array)
                avg_val = int(sum(integer_array) / len(integer_array))

                print(f"Maximum of {file_name} is {max_val}")
                print(f"Minimum of {file_name} is {min_val}")
                print(f"Average of {file_name} is {avg_val}")

        except Exception as e: # Handling processing problems
            print(f"Error occurred while processing file '{file_name}': {e}")

    else: # If file is not in directory
        print(f"File '{file_name}' does not exist.")


        
def handle_put_request(data):
    print("Received put request from client")

    # Parse the command
    opcode = data[:3] # opcode 
    file_length_binary = data[3:8] # get file length binary
    #TODO: find logic to parse file_name binary in the array 
    # probably by getting length of file_name_binary
    # file_name_binary = data[8:] # get file name binary 
    # file_size_binary = 
    #  + file_data_binary

    file_length = int(file_length_binary, 2) # convert binary to int for file length
    
    # Decode file name binary to retrieve the file name
    file_name = ''.join(chr(int(file_name_binary[i:i+8], 2)) for i in range(0, len(file_name_binary), 8))

    #using file name, open file and do the summary

    # print("Received Command from TCP Client:")
    # print(f"Opcode: {opcode}")
    # print(f"File Length Binary: {file_length_binary}")
    # print(f"File Length: {file_length}")
    # print(f"File Name: {file_name}")


def handle_tcp_client(client, addr):
    print("Connected by TCP at ", addr)
    print("Success")

    while True:
        data = client.recv(1024).decode()
        if not data: # checks if data is empty
            break

        # Check command opcode and handle requests based of it
        opcode = data[:3]

        match (opcode):
            case "000":
                handle_put_request(data)
                # handle put
            case "001":
                print ("Received get request from client")
                # handle get
            case "010":
                print ("Received change request from client")
                # handle change
            case "011":
                print ("Received summary request from client")
                handle_summary_request(data)
            case "100":
                print ("Received help request from client")
                # handle help
            case _:
                # handle invalid opcode
                print ("Received invalid request. Try again.")
                
        
        
        # if data == "10000000": 
        #     print ("Help me pretty please")
        #     continue

        # else:
        #     opcode = data[:3]
        #     file_length_binary = data[3:8]
        #     file_name_binary = data[8:]

        #     file_length = int(file_length_binary, 2)
        #     # Decode file name binary to retrieve the file name
        #     file_name = ''.join(chr(int(file_name_binary[i:i+8], 2)) for i in range(0, len(file_name_binary), 8))

        #     # Perform actions based on the parsed command
        #     # Example: Print the parsed command details
        #     print("Received Command from TCP Client:")
        #     print(f"Opcode: {opcode}")
        #     print(f"File Length Binary: {file_length_binary}")
        #     print(f"File Length: {file_length}")
        #     print(f"File Name: {file_name}")

    client.close()

def tcp_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_socket:
        tcp_socket.bind((HOST,PORT))
        tcp_socket.listen(0)

        print ("Server is waiting for TCP client connection")

        # while True:
        #     client, addr = tcp_socket.accept()
        #     client_thread = threading.Thread(target=handle_tcp_client, args=(client, addr))
        #     client_thread.start()

        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
            while True:
                client, addr = tcp_socket.accept()
                executor.submit(handle_tcp_client, client, addr)
                print("Accepted a connection")
                time.sleep(10)

        
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

time.sleep(10)