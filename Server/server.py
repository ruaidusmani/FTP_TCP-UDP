"""
Carl Nakad (40210586), Ruaid Usmani (40212428)

Server File to handle requests from clients and send response

"We certify that this submission is the original work of members
of the group and meets the Faculty's Expectations of Originality.”
"""

import socket
import threading
import concurrent.futures
import time
import os
import string
import sys
sys.path.insert(0, '../Controller')
from control_module import controller

HOST = "127.0.0.1" #localhost
PORT = 20000 # listening port

# MAX_THREADS = 10

def handle_summary_request(data):
    global debug_flag
    # Parse the command
    opcode = data[:3] # opcode 
    file_length_binary = data[3:8] # get file length binary
    file_name_binary = data[8:] # get file name binary

    file_length = int(file_length_binary, 2) # convert binary to int for file length
    
    # Decode file name binary to retrieve the file name
    file_name = ''.join(chr(int(file_name_binary[i:i+8], 2)) for i in range(0, len(file_name_binary), 8))

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

        summary_file_contents = maximum_string + "\n" + minimum_string + "\n" + average_string

        summary_file_name = "summary_" + file_name.split('.')[0] + ".txt"
        
        with open(summary_file_name, 'w') as summary_file:
            summary_file.write(summary_file_contents)

        # Send file to client
        res_code = "010"
        if (debug_flag == 1):
            print("File NAME = " + file_name)
            print("Res code = " + res_code)

        file_length_binary = controller.get_file_length(summary_file_name)
        file_name_binary = controller.get_file_name_binary(summary_file_name)
        file_size_binary = controller.get_file_size_binary(summary_file_name)
        file_data_binary = controller.get_file_data_binary(summary_file_name)

        if os.path.exists(summary_file_name):
            os.remove(summary_file_name)
        else:
            if (debug_flag == 1):
                print("The file does not exist")
            return "011" + "00000"
        # Response message send to client
        response_message = res_code + file_length_binary + file_name_binary + file_size_binary + file_data_binary.decode('utf-8')

        # print (response_message)
        return response_message
            
    else: # If file is not in directory
        if (debug_flag == 1):
            print(f"File '{file_name}' does not exist.")
        return "011" + "00000"

def handle_get_request(data):
    global debug_flag
    if (debug_flag == 1):
        print("Received get request from client")

    # Parse the command
    opcode = data[:3] # opcode
    file_length_binary = data[3:8] # get file length binary
    file_name_binary = data[8:] # get file name binary

    file_length = int(file_length_binary, 2) # convert binary to int for file length

    # Decode file name binary to retrieve the file name
    file_name = ''.join(chr(int(file_name_binary[i:i+8], 2)) for i in range(0, len(file_name_binary), 8))

    if (debug_flag == 1):
        print("File NAME = " + file_name)

    if os.path.exists(file_name): # check if file exists in directory

        # Send file to client
        res_code = "001"
        if (debug_flag == 1):
            print("Res code = " + res_code)

        file_length_binary = controller.get_file_length(file_name)
        file_name_binary = controller.get_file_name_binary(file_name)
        file_size_binary = controller.get_file_size_binary(file_name)
        file_data_binary = controller.get_file_data_binary(file_name)
        
        # Response message send to client
        response_message = res_code + file_length_binary + file_name_binary + file_size_binary

        return response_message, file_data_binary
    
    else: # If file is not in directory
        if (debug_flag == 1):
            print(f"File '{file_name}' does not exist.")
        return "011" + "00000", None

        
def handle_put_request(data, client):
    global debug_flag


    # data_decoded = data[].decode()
    # Parse the command
    opcode = data[:3].decode() # opcode 


    file_length_binary = data[3:8].decode() # get file length binary


    file_length = int(file_length_binary, 2) # convert binary to int for file length
    file_length_byte = (file_length-1) * 8 # get file length in bytes


    file_name_binary = data[8:8+file_length_byte].decode() # get file name binary
  
    # Decode file name binary to retrieve the file name
    file_name = ''.join(chr(int(file_name_binary[i:i+8], 2)) for i in range(0, len(file_name_binary), 8))

    file_size_binary = data[8+file_length_byte:8+file_length_byte+32].decode() # get file size binary
    file_size = int(file_size_binary, 2) # convert binary to int for file length


    file_data = data[8+file_length_byte+32:]

    # print(f"File data2: {client.recv(file_size)}")
    
    if (debug_flag == 1):
        print("Received put request from client")
        print(f"Opcode: {opcode}")
        print(f"File Length Binary: {file_length_binary}")
        print(f"File length in bytes: {file_length_byte}")
        print(f"File name binary: {file_name_binary}")
        print(f"File size binary: {file_size_binary}")
        print(f"File size: {file_size}")
        print(f"File data1: {file_data}")


    if (file_size > 1024):
        while (file_size > 0):
            if (file_size < 1024):
                try:
                    file_data += client.recv(file_size)
                except TimeoutError:
                    break
                break
            file_data += client.recv(1024)
            file_size -= 1024
            if (debug_flag == 1):
                print (f"File size: {file_size}")
    elif (len(file_data) != file_size):
        file_data = client.recv(file_size)

    if (debug_flag == 1):
        print(f"Opcode: {opcode}")
        print(f"File Length Binary: {file_length_binary}")
        print(f"File Length: {file_length}")
        print(f"File Name: {file_name}")
        print(f"File Data: {file_data}")

    # write to file function
    res_code = controller.file_write(file_name, file_data)

    # Send response to client
    if (debug_flag == 1):
        print("Res code = " + res_code)
    
    # Response message send to client
    response_message = res_code + "00000"
    
    if (debug_flag == 1):
        print (response_message)

    return response_message

def handle_change_request(data):
    global debug_flag



    # Parse the command
    opcode = data[:3] # opcode


    old_file_length_binary = data[3:8] # get file length binary


    old_file_length = int(old_file_length_binary, 2) # convert binary to int for file length
    old_file_length_byte = (old_file_length-1) * 8 # get file length in bytes


    old_file_name_binary = data[8:8+old_file_length_byte] # get file name binary

    # Decode file name binary to retrieve the file name
    old_file_name = ''.join(chr(int(old_file_name_binary[i:i+8], 2)) for i in range(0, len(old_file_name_binary), 8))

    new_file_length_binary = data[8+old_file_length_byte:8+old_file_length_byte+5] # get file length binary
 

    new_file_length = int(new_file_length_binary, 2) # convert binary to int for file length
    new_file_length_byte = (new_file_length-1) * 8 # get file length in bytes


    new_file_name_binary = data[8+old_file_length_byte+5:] # get file name binary

    # Decode file name binary to retrieve the file name
    new_file_name = ''.join(chr(int(new_file_name_binary[i:i+8], 2)) for i in range(0, len(new_file_name_binary), 8))



    if (debug_flag == 1):
        print("Received change request from client") 
        print(f"Opcode: {opcode}")
        print(f"File Length Binary: {old_file_length_binary}")
        print(f"File length in bytes: {old_file_length_byte}")
        print(f"File name binary: {old_file_name_binary}")
        print(f"File Length Binary: {new_file_length_binary}")
        print(f"File length in bytes: {new_file_length_byte}")
        print(f"File name binary: {new_file_name_binary}")


        # print("Received Command from TCP Client:")
        print(f"Opcode: {opcode}")
        print(f"Old file name: {old_file_name}")
        print(f"New file name: {new_file_name}")
    

    if (os.path.exists(new_file_name)):
        response_message = "101" + "00000"
        return response_message
    
    os.rename(old_file_name, new_file_name)

    # Send response to client
    res_code = "000"
    if (debug_flag == 1):
        print("Res code = " + res_code)
    
    # Response message send to client
    response_message = res_code + "00" + opcode

    return response_message

def handle_help_request(data):
    global debug_flag
    # Parse the command
    opcode = data[:3] # opcode
    help_response_string = "bye change get help put summary"

    # help_msg_binary_length = help_binary_length(len(help_response_string))
    
    # Will give length of 31 which is 11111 in binary
    help_msg_binary_length = format(len(help_response_string), '05b')

    help_response_string_binary = controller.string_to_binary(help_response_string)
    
    if (debug_flag == 1):
        print ("Help response string binary = " + help_response_string_binary)
    
    # Response message format
    res_code = "110"
    length = help_msg_binary_length
    help_data = help_response_string_binary

    # Response message send to client
    response_message = res_code + length + help_data

    return response_message

def handle_tcp_client(client, addr):
    global debug_flag
    print("Connected by TCP at ", addr)
    print("Success")

    while True:
        try:
            data = client.recv(1024)
        except ConnectionResetError:
            print("Client disconnected")
            return
        except TimeoutError:
            continue

        if not data: # checks if data is empty
            print("Disconnected")
            break

        # Check command opcode and handle requests based of it
        try:
            opcode = data[:3].decode()
        except UnicodeDecodeError:
            print("Invalid opcode")
            continue

        match (opcode):
            case "000":
                if (debug_flag == 1):
                    print ("Received put request from client")
                response_msg = handle_put_request(data, client)
            case "001":
                if (debug_flag == 1):
                    print ("Received get request from client")
                response_msg, response_data = handle_get_request(data.decode())
            case "010":
                if (debug_flag == 1):
                    print ("Received change request from client")
                response_msg = handle_change_request(data.decode())
            case "011":
                if (debug_flag == 1):
                    print ("Received summary request from client")
                response_msg = handle_summary_request(data.decode())
            case "100":
                if (debug_flag == 1):
                    print ("Received help request from client")
                response_msg = handle_help_request(data.decode())
            case _:
                # handle invalid opcode
                if (debug_flag == 1):
                    print ("Received invalid request. Try again.")
                response_msg = "100" + "00000"
        
        
        client.sendall(response_msg.encode())
        if (opcode == "001" and response_data is not None):
            if (debug_flag == 1):
                print("Response data = ", response_data)
            client.sendall(response_data)


def tcp_server():
    global debug_flag
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print("TCP Server listening")

        while True:
            client_socket, addr = server_socket.accept()
            client_thread = threading.Thread(target=handle_tcp_client, args=(client_socket, addr))
            client_socket.settimeout(1)
            client_thread.start()
            
def udp_server():
    global debug_flag
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        server_socket.bind((HOST, PORT))
        print("UDP Server listening")

        while True:
            data, addr = server_socket.recvfrom(1024)
            print(f"UDP message from {addr}: {data}")

            if not data: # checks if data is empty
                print("Data empty")
                continue

            print(f"Received message from {addr}: {data}")

            # Check command opcode and handle requests based on it
            opcode = data[:3].decode()

            match (opcode):
                case "000":
                    if (debug_flag == 1):
                        print ("Received put request from client")
                    response_msg = handle_put_request(data, server_socket)
                case "001":
                    if (debug_flag == 1):
                        print ("Received get request from client")
                    response_msg, response_data = handle_get_request(data.decode())
                case "010":
                    if (debug_flag == 1):
                        print ("Received change request from client")
                    response_msg = handle_change_request(data.decode())
                case "011":
                    if (debug_flag == 1):
                        print ("Received summary request from client")
                    response_msg = handle_summary_request(data.decode())
                case "100":
                    if (debug_flag == 1):
                        print ("Received help request from client")
                    response_msg = handle_help_request(data.decode())
                case _:
                    # handle invalid opcode
                    if (debug_flag == 1):
                        print ("Received invalid request. Try again.")
                    response_msg = "100" + "00000"
                    
            # response_msg_bytes = str.encode()
            server_socket.sendto(response_msg.encode(), addr)
            if (opcode == "001" and response_data is not None):
                send_file_via_udp(response_data, addr[0], addr[1])
                # server_socket.sendto(response_data, addr)

def send_file_via_udp(file_data_binary, ip_address, port_number):
    CHUNK_SIZE = 1024  # Define a chunk size (in bytes)

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
        # Splitting the file_data_binary into chunks
        for i in range(0, len(file_data_binary), CHUNK_SIZE):
            chunk = file_data_binary[i:i+CHUNK_SIZE]
            client_socket.sendto(chunk, (ip_address, port_number))


debug_flag = int(sys.argv[1])
if (debug_flag == 1):
    print("Debug mode ON")
else: 
    print("Debug mode OFF")

print("Starting server...")
print("ip address: " + HOST)
print("port number: " + str(PORT))
tcp_thread = threading.Thread(target=tcp_server, daemon=True)
udp_thread = threading.Thread(target=udp_server, daemon=True)

try:
    tcp_thread.start() 
    udp_thread.start()

    while True:
        pass

except (KeyboardInterrupt, SystemExit):
    print("Server is shutting down...")
    sys.exit()
