import socket 
import os

def get_opcode(command):
    command_breakdown = command.split()
    user_command = command_breakdown[0]
    opcode = ""

    if user_command == "put":
        opcode = "000"
    elif user_command == "get":
        opcode = "001"
    elif user_command == "change":
        opcode = "010"
    elif user_command == "summary":
        opcode = "011"
    elif user_command == "help":
        opcode = "100"

    return opcode

def get_file_length(command_file_name):
    file_length = len(command_file_name) + 1
    #convert file length to string

    binary_string = format(file_length, '05b')

    # print ("FILE LENGTH = " + str(file_length))  
    if (file_length < 32):
        file_length_binary = format(file_length, '05b')
    else:
        file_length_binary = -1  # -1 means that the file name is too long
    return file_length_binary

def get_file_name_binary(command_file_name):
    binary_string = ''.join(format(ord(char), '08b') for char in command_file_name)
    return binary_string

def get_file_size_binary(file):
    file_size = os.path.getsize(file) # get file size in bytes
    file_size_binary = format(file_size, '032b') # convert this to 32-bit (4 byte) binary
    return str(file_size_binary)

def get_file_data_binary(file):
    with open(file, 'r') as f: # open file in binary mode
        file_data = f.read() # read file data

    file_data_binary = ""
    for i in range(0, len(file_data)):
        # convert each character to binary
        file_data_binary += format(ord(file_data[i]), '08b')

    return str(file_data_binary)

# def handle_put_request(file):
#     file_size = os.path.getsize(file) # get file size in bytes
#     file_size_binary = format(file_size, '032b') # convert this to 32-bit (4 byte) binary

#     # Get file data
#     with open(file, 'rb') as f: # open file in binary mode
#         file_data_binary = f.read() # read file data
        
#     return file_size_binary, file_data_binary

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


def response():
    data = socket.recv(4096).decode()  # Adjust the buffer size as needed

    if data:
        res_code = data[:3]

        if res_code == "000":
            print("File successfully transferred.")
        elif res_code == "010":
            summary_response(data)

    else:
        print("No data received from the server")
        return


def summary_response(data):
    # print("we in here")

    # print("problem.")

    # # try:
    # # Receive data
    # data = socket.recv(4096).decode()  # Adjust the buffer size as needed

    # if data:
        # parse msg to get file name and file size
    res_code = data[:3]
    res_file_name_length_binary = data[3:8]
    res_file_name_length = int(res_file_name_length_binary, 2)
    print("res_file_name_binary_length = ", res_file_name_length)
    res_file_name_byte_length = (res_file_name_length-1) * 8

    res_file_name = data[8:8+res_file_name_byte_length]
    print("length of binary string of res_file_name: ", len(res_file_name))
    print("res_file_name bn: ", res_file_name)
    res_file_name_str = binary_to_string(res_file_name)
    print("res_file_name str: ", res_file_name_str)

    res_file_size = data[8+res_file_name_byte_length:8+res_file_name_byte_length+32]
    print("res_file_size bn: ", res_file_size)

    res_file_data = data[8+res_file_name_byte_length+32:]
    print("res_file_data bn: ", res_file_data)

    res_file_data = ''.join(chr(int(res_file_data[i:i+8], 2)) for i in range(0, len(res_file_data), 8))
    
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

def help_response():
    print("we in here")
    data = socket.recv(4096).decode()  # Adjust the buffer size as needed

    if data:
        # parse msg to get file name and file size
        res_code = data[:3]
        res_length = data[3:8]
        res_data = data[8:]

        # convert res_data to string
        res_data = binary_to_string(res_data)
    
        help_msg = "Commands are: " + res_data
        print(help_msg)


###### MAIN ######

# Ask user for decision on TCP or UDP
# protocol = protocol_input()
protocol = "TCP"
# print(protocol)

# IP Address and Port Number Input
# ip_address, port_number = get_ip_address_port()
ip_address, port_number = "127.0.0.1", int("12000")
print(ip_address)
print(port_number)

# Connect to server based on protocol
# TODO: Uncomment this after server.py created
if (protocol == "TCP"):
    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.connect((ip_address, port_number))
    print("TCP Server-Client Connected")

elif (protocol == "UDP"):
    socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print("UDP Server-Client Connected")

# print list of commands
#TODO: Implement this in the help command coming from the server
print ("Commands are: bye, change, get, help, put, summary")

# main loop
in_progress = True
while in_progress:
    # Ask user for command
    print("Enter command: ")
    full_command = input("")
    command_array = full_command.split()

    # Process the commands
    if command_array[0] in ["help", "bye"]: # commands with no file name
        if len(command_array) == 1: # check if there is only one command
            
            if command_array[0] == "bye": # closes client session
                print("Session is terminated.") 
                socket.close()
                in_progress = False

            elif command_array[0] == "help": # help message
                opcode = get_opcode(command_array[0]) # get opcode for command
                
                #Send command to server
                command = opcode + "00000"
                socket.send(command.encode())
                help_response()

        else: # invalid command handling
            print("Invalid command, please try again.")
            continue

    elif command_array[0] in ["put", "get", "summary"]: # commands with 1 file name
        if len(command_array) == 2: # check if there are 2 commands
        
            opcode = get_opcode(command_array[0]) # get opcode for command
            file1_length_binary = get_file_length(command_array[1]) # get file name size in binary
            
            if file1_length_binary != -1: # check if file name is of appropriate length
                file_name_binary = get_file_name_binary(command_array[1]) # get file name binary
            else: 
                print("File name is too long, please try again.")
                continue


            if (command_array[0] == "put"):
                file_size_binary = get_file_size_binary(command_array[1])
                file_data_binary = get_file_data_binary(command_array[1])
                print("file_length_binary: ", file1_length_binary)
                print("file_name_binary: ", file_name_binary)
                print("file_size_binary: ", file_size_binary)
                print("file_data_binary: ", file_data_binary)

                command = opcode + file1_length_binary + file_name_binary + file_size_binary + file_data_binary
            else:  
                command = opcode + file1_length_binary + file_name_binary

            socket.send(command.encode())
            response()
            

        else: # invalid command handling
            print("Invalid command, please try again.")
            continue

    elif command_array[0] == "change": # commands with 2 file names
        if len(command_array) == 3:
            opcode = get_opcode(command_array[0]) # get opcode for command
            file1_length_binary = get_file_length(command_array[1]) # get file1 name size in binary
            file2_length_binary = get_file_length(command_array[2]) # get file2 name size in binary

            if file1_length_binary != -1 and file2_length_binary != -1: # check if file name is of appropriate length
                file1_name_binary = get_file_name_binary(command_array[1])
                file2_name_binary = get_file_name_binary(command_array[2])

            else: # returns -1 for having a long file_name
                print("One of the two file names is too long, please try again.")
                continue

            command = opcode + file1_length_binary + file1_name_binary + file2_length_binary + file2_name_binary

        else: # invalid command handling
            print("Invalid command, please try again.")
            continue

    else: # completely wrong command handling
        print("Invalid command, please try again.")
        continue