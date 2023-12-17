import socket 
import os
import sys
import time
sys.path.insert(0, '../Controller')
from control_module import controller

client_socket = None

def protocol_input():
    while True:
        try:
            protocol_input = int(input("Press 1 for TCP, Press 2 for UDP: "))
            if protocol_input not in [1, 2]:
                raise ValueError
        except ValueError:
            print("Invalid Response.")
            continue
        else:
            break
    if (protocol_input == 1):
        protocol = "TCP"
    elif (protocol_input == 2):
        protocol = "UDP"
    return protocol

def get_ip_address_port():
    while True:
        try:
            ip, port = input("Provide IP address and Port Number: ").split()
            # Check if the IP address is valid
            socket.inet_aton(ip)
            
            # Check if the port is a valid integer within the range
            port = int(port)
            if 0 < port < 65536:
                return ip, port
            else:
                print("Port number should be between 1 and 65535. Try again.")
        except ValueError:
            print("Please enter both IP address and port number separated by a space. Try again.")
        except socket.error:
            print("Invalid IP address or port number. Try again.")

def binary_to_string(binary_string):
    # Split the binary string into 8-bit chunks
    chunks = [binary_string[i:i+8] for i in range(0, len(binary_string), 8)]

    # Convert each 8-bit chunk to a character
    characters = [chr(int(chunk, 2)) for chunk in chunks]

    # Join the characters to form a string
    result_string = ''.join(characters)

    return result_string

def send_request():
    if (protocol == "TCP"):
        client_socket.sendall(command.encode())
    elif (protocol == "UDP"):
        client_socket.sendto(command.encode(), (ip_address, port_number))

def recv_response():
    if (protocol == "TCP"):
        try:
            data, none = client_socket.recvfrom(1024)
        except socket.timeout:
            print("Server is not responding.")
            return
    elif (protocol == "UDP"):
        data, client = client_socket.recvfrom(1024)
        # data = msg.decode()
    return data

def response():
    # data = socket.recv(4096).decode()  # Adjust the buffer size as needed
    try:
        data = recv_response()
        print("data: ", data)
        if data:
            try:
                res_code = data.decode()[:3]
                res_op_code = data.decode()[-3:]
            except AttributeError:
                res_code = data[:3]
                res_op_code = data[-3:]

            print("res_code: ", res_code, "res_op_code: ", res_op_code)

            if res_code == "000":
                if (res_op_code == "010"):
                    print("File name has been changed.")
                else:
                    print("File has been uploaded successfully.")
            elif res_code == "001":
                get_response(data)
            elif res_code == "010":
                summary_response(data)
            elif res_code == "011":
                print("File does not exist on server.")
            elif res_code == "100":
                print("Error - Unknown Request")
            elif res_code == "101":
                print("Unsuccessful change")
            elif res_code == "110":
                help_response(data)

        else:
            print("No data received from the server")
            return
    except ConnectionResetError:
        print("Failed to receive response from server.")
        return


def summary_response(data):
    # print("we in here")

    # print("problem.")

    # # try:
    # # Receive data
    # data = socket.recv(4096).decode()  # Adjust the buffer size as needed

    # if data:
        # parse msg to get file name and file size
    res_code = data[:3].decode()
    res_file_name_length_binary = data[3:8].decode()
    res_file_name_length = int(res_file_name_length_binary, 2)
    print("res_file_name_binary_length = ", res_file_name_length)
    res_file_name_byte_length = (res_file_name_length-1) * 8

    res_file_name = data[8:8+res_file_name_byte_length].decode()
    print("length of binary string of res_file_name: ", len(res_file_name))
    print("res_file_name bn: ", res_file_name)
    res_file_name_str = binary_to_string(res_file_name)
    print("res_file_name str: ", res_file_name_str)

    res_file_size = data[8+res_file_name_byte_length:8+res_file_name_byte_length+32].decode()
    print("res_file_size bn: ", res_file_size)

    res_file_data = data[8+res_file_name_byte_length+32:].decode()
    print("res_file_data bn: ", res_file_data)

    # res_file_data = ''.join(chr(int(res_file_data[i:i+8], 2)) for i in range(0, len(res_file_data), 8))
    
    # print response
    print("Response from server:")
    print(f"Response Code: {res_code}")
    print(f"File Name Length: {res_file_name_length}")
    print(f"File Name: {res_file_name_str}")
    print(f"File Size: {res_file_size}")
    print(f"File Data: {res_file_data}")

    # Store file content into a file
    file = open(res_file_name_str, "w")
    file.write(res_file_data)
    file.close()

    print("Summary Done")
    # else:
        # print("No data received from the server")
        # return

def help_response(data):
    # data = socket.recv(4096).decode()  # Adjust the buffer size as needed

    # if data:
        # parse msg to get file name and file size
    res_code = data[:3]
    res_length = data[3:8]
    res_data = data[8:]

    # convert res_data to string
    res_data = binary_to_string(res_data)

    help_msg = "Commands are: " + res_data
    print(help_msg)

def get_response(data):
    # Parse the command
    opcode = data[:3].decode() # opcode 
    print(f"Opcode: {opcode}")

    file_length_binary = data[3:8].decode() # get file length binary
    print(f"File Length Binary: {file_length_binary}")

    file_length = int(file_length_binary, 2) # convert binary to int for file length
    file_length_byte = (file_length-1) * 8 # get file length in bytes
    print(f"File length in bytes: {file_length_byte}")

    file_name_binary = data[8:8+file_length_byte].decode() # get file name binary
    print(f"File name binary: {file_name_binary}")
    # Decode file name binary to retrieve the file name
    file_name = ''.join(chr(int(file_name_binary[i:i+8], 2)) for i in range(0, len(file_name_binary), 8))

    file_size_binary = data[8+file_length_byte:8+file_length_byte+32].decode() # get file size binary
    file_size = int(file_size_binary, 2) # convert binary to int for file length
    print(f"File size binary: {file_size_binary}")
    print(f"File size: {file_size}")
    file_data = b''

    print("Receiving file data...")
    if (file_size > 1024):
        while (file_size > 0):
            file_data += client_socket.recv(1024)
            file_size -= 1024
    else:
        file_data += client_socket.recv(1024)

    with open(file_name, 'wb') as file:
        file.write(file_data)

    print(f"{file_name} has been downloaded successfully.")

    file_data_binary = data[8+file_length_byte+32:] # get file data binary
    print(f"File data binary: {file_data_binary}")

    print(f"Opcode: {opcode}")
    print(f"File Length Binary: {file_length_binary}")
    print(f"File Length: {file_length}")
    print(f"File Name: {file_name}")
    print(f"File Data: {file_data}")

def send_file_via_udp(file_data_binary, ip_address, port_number):
    CHUNK_SIZE = 1024  # Define a chunk size (in bytes)

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
        # Splitting the file_data_binary into chunks
        for i in range(0, len(file_data_binary), CHUNK_SIZE):
            chunk = file_data_binary[i:i+CHUNK_SIZE]
            client_socket.sendto(chunk, (ip_address, port_number))

def create_socket(protocol):
    global client_socket
    if protocol == "TCP":
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.settimeout(5.0)
        client_socket.connect((ip_address, port_number))
        print("TCP Server-Client Connected")
    elif protocol == "UDP":
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print("UDP Server-Client Connected")
###### MAIN ######

# Ask user for decision on TCP or UDP
protocol = protocol_input()

# IP Address and Port Number Input
# ip_address, port_number = get_ip_address_port()
ip_address, port_number = "127.0.0.1", int("12000")
# ip_address, port_number = "10.0.0.54", int("12000")
print(ip_address)
print(port_number)

# Connect to server based on protocol
# TODO: Uncomment this after server.py created
create_socket(protocol)

# print list of commands
#TODO: Implement this in the help command coming from the server
print ("Commands are: bye, change, get, help, put, summary")


# main loop
in_progress = True
while in_progress:
    try:
        # Ask user for command
        print("Enter command: ")
        full_command = input("")
        command_array = full_command.split()


        # Process the commands
        if command_array[0] in ["help", "bye"]: # commands with no file name
            if len(command_array) == 1: # check if there is only one command
                if command_array[0] == "bye": # closes client session
                    print("Session is terminated.") 
                    client_socket.close()
                    in_progress = False

                elif command_array[0] == "help": # help message
                    opcode = controller.get_opcode(command_array[0]) # get opcode for command
                    
                    #Send command to server
                    command = opcode + "00000"
                    print("PROTOCOL USED = ", protocol) 
                    try:
                        send_request()
                        print("PROTOCOL RECV = ", protocol) 
                        # socket.send(command.encode())
                    except ConnectionResetError:
                        print("No Server. Exiting!")
                        exit()
                        
                    # send_request()
                    # socket.send(command.encode())
                    print("PROTOCOL RECV = ", protocol) 
                    response()

            else: # invalid command handling
                print("Invalid command, please try again.")
                continue

        elif command_array[0] in ["put", "get", "summary"]: # commands with 1 file name
            if len(command_array) == 2: # check if there are 2 commands
                opcode = controller.get_opcode(command_array[0]) # get opcode for command
                file1_length_binary = controller.get_file_length(command_array[1]) # get file name size in binary
                
                if file1_length_binary != -1: # check if file name is of appropriate length
                    file_name_binary = controller.get_file_name_binary(command_array[1]) # get file name binary
                else: 
                    print("File name is too long, please try again.")
                    continue

                
                if (command_array[0] == "put"):
                    file_size_binary = controller.get_file_size_binary(command_array[1])
                    
                    if (file_size_binary == -1):
                        print("File not found.")
                        continue
                    file_data_binary = controller.get_file_data_binary(command_array[1])
                    print("file_length_binary: ", file1_length_binary)
                    print("file_name_binary: ", file_name_binary)
                    print("file_size_binary: ", file_size_binary)
                    print("file_data_binary: ", file_data_binary)

                    command = opcode + file1_length_binary + file_name_binary + file_size_binary
                    
                else:  
                    command = opcode + file1_length_binary + file_name_binary

                print("PROTOCOL USED = ", protocol) 
                send_request()
    
                if (command_array[0] == "put"):
                    if (protocol == "TCP"):
                        print("PEPE")
                        client_socket.sendall(file_data_binary)
                    else:
                        send_file_via_udp(file_data_binary, ip_address, port_number)
                        # client_socket.sendto(file_data_binary, (ip_address, port_number))
                    
                # socket.send(command.encode())
                print("PROTOCOL RECV = ", protocol)
                response()
                

            else: # invalid command handling
                print("Invalid command, please try again.")
                continue

        elif command_array[0] == "change": # commands with 2 file names
            if len(command_array) == 3:
                opcode = controller.get_opcode(command_array[0]) # get opcode for command
                file1_length_binary = controller.get_file_length(command_array[1]) # get file1 name size in binary
                file2_length_binary = controller.get_file_length(command_array[2]) # get file2 name size in binary

                if file1_length_binary != -1 and file2_length_binary != -1: # check if file name is of appropriate length
                    file1_name_binary = controller.get_file_name_binary(command_array[1])
                    file2_name_binary = controller.get_file_name_binary(command_array[2])

                else: # returns -1 for having a long file_name
                    print("One of the two file names is too long, please try again.")
                    continue

                command = opcode + file1_length_binary + file1_name_binary + file2_length_binary + file2_name_binary

                send_request()
                # socket.send(command.encode())
                response()

            else: # invalid command handling
                print("Invalid command, please try again.")
                continue

        else: # completely wrong command handling
            print("Invalid command, please try again.")
            continue
    except KeyboardInterrupt:
        print("Session is terminated.") 
        client_socket.close()
        in_progress = False
        sys.exit()