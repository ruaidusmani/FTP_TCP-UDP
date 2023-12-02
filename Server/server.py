import socket
import threading
import concurrent.futures
import time
import os
import string

HOST = "127.0.0.1" #localhost
PORT = 12000 # listening port

MAX_THREADS = 10

def get_file_length(file_name):
    file_length = len(file_name) + 1
    #convert file length to string

    binary_string = format(file_length, '05b')

    # print ("FILE LENGTH = " + str(file_length))  
    if (file_length < 32):
        file_length_binary = format(file_length, '05b')
    else:
        file_length_binary = -1  # -1 means that the file name is too long
    return str(file_length_binary)

def get_file_name_binary(file_name):
    binary_string = ''.join(format(ord(char), '08b') for char in file_name)
    print ("Binary string in func: ")
    print (binary_string)

    return str(binary_string)

def get_file_data_binary(file_name):
    with open(file_name, 'r') as f: # open file in binary mode
        file_data = f.read() # read file data

    file_data_binary = ""
    for i in range(0, len(file_data)):
        # convert each character to binary
        file_data_binary += format(ord(file_data[i]), '08b')

    return str(file_data_binary)


def get_file_size_binary(file):
    file_size = os.path.getsize(file) # get file size in bytes
    file_size_binary = format(file_size, '032b') # convert this to 32-bit (4 byte) binary
    return str(file_size_binary)


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
        # try: 
        with open(file_name, 'r') as file: # Open and read the file content
            file_content = file.read()
            integer_array = [int(i) for i in file_content.split(',')] # store text in array of integers

            # Perform max, min, and average 
            max_val = max(integer_array)
            min_val = min(integer_array)
            avg_val = int(sum(integer_array) / len(integer_array))

            maximum_string = f"Maximum of {file_name} is {max_val}"
            minimum_string = f"Minimum of {file_name} is {min_val}"
            average_string = f"Average of {file_name} is {avg_val}"

            # print(maximum_string)
            # print(minimum_string)
            # print(average_string)

            summary_file_contents = maximum_string + "\n" + minimum_string + "\n" + average_string

            summary_file_name = "summary_" + file_name.split('.')[0] + ".txt"
            
            with open(summary_file_name, 'w') as summary_file:
                summary_file.write(summary_file_contents)

            # Send file to client
            res_code = "010"
            print("Res code = " + res_code)

            # NOT PRINTING
            file_length_binary = get_file_length(summary_file_name)
            file_name_binary = get_file_name_binary(summary_file_name)
            file_size_binary = get_file_size_binary(summary_file_name)
            file_data_binary = get_file_data_binary(summary_file_name)

            print ("File length binary = " + file_length_binary)
            print ("File name binary = " + file_name_binary)
            print ("File size binary = " + file_size_binary)
            print ("File data binary = " + file_data_binary)


            # Response message send to client
            response_message = res_code + file_length_binary + file_name_binary + file_size_binary + file_data_binary
            # Send response message to client
            print("Sending")
            
            print("Sent")

            return response_message
            
            

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


# def handle_help_request():


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
                response_msg = handle_put_request(data)
                # handle put
            case "001":
                print ("Received get request from client")
                # handle get
            case "010":
                print ("Received change request from client")
                # handle change
            case "011":
                print ("Received summary request from client")
                response_msg = handle_summary_request(data)
            case "100":
                print ("Received help request from client")
                # handle help
            case _:
                # handle invalid opcode
                print ("Received invalid request. Try again.")
                
        return response_msg

def tcp_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_socket:
        tcp_socket.bind((HOST,PORT))
        tcp_socket.listen(0)

        print ("Server is waiting for TCP client connection")

        while True:
            # Accept incoming client connection
            client_socket, client_address = tcp_socket.accept()
            print(f"Accepted connection from {client_address}")

            # Handle the client connection in a separate thread or function
            response = handle_tcp_client(client_socket, client_address)

            client_socket.send(response.encode())

        # while True:
        #     client, addr = tcp_socket.accept()
        #     client_thread = threading.Thread(target=handle_tcp_client, args=(client, addr))
        #     client_thread.start()

        # with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        #     while True:
        #         client, addr = tcp_socket.accept()
        #         executor.submit(handle_tcp_client, client, addr)
        #         print("Accepted a connection")
        #         time.sleep(10)

        
        # conn,addr = tcp_socket.accept()
        
        # with conn:
        #     print("Connected by TCP at ", addr)
        #     print("Success")
            

# def udp_server():
#     with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
#         udp_socket.bind((HOST,PORT))
#         print("UDP Server is waiting for client connection")
#         conn,addr = udp_socket.recvfrom(1024)
#         with conn:
#             print("Connected by UDP at ", addr)
#             print("Success")


# tcp_thread = threading.Thread(target=tcp_server)
# udp_thread = threading.Thread(target=udp_server)

# tcp_thread.start()
# udp_thread.start()

# time.sleep(10)

tcp_server()