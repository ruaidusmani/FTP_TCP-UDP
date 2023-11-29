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

    print ("FILE LENGTH = " + str(file_length))  
    if (file_length < 32):
        file_length_binary = format(file_length, '05b')
    else:
        file_length_binary = -1  # -1 means that the file name is too long
    return file_length_binary

def get_file_name_binary(command_file_name):
    binary_string = ''.join(format(ord(char), '08b') for char in command_file_name)
    return binary_string

def handle_put_request(file):
    file_size = os.path.getsize(file) # get file size in bytes
    file_size_binary = format(file_size, '032b') # convert this to 32-bit (4 byte) binary

    # Get file data
    with open(file, 'rb') as f: # open file in binary mode
        file_data_binary = f.read() # read file data
        
    return file_size_binary, file_data_binary

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


###### MAIN ######

# Ask user for decision on TCP or UDP
protocol = protocol_input()
print(protocol)

# IP Address and Port Number Input
ip_address, port_number = get_ip_address_port()
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


            if (command_array == "put"):
                file_size_binary, file_data_binary = handle_put_request(command_array[1])
                command = opcode + file1_length_binary + file_name_binary + file_size_binary + file_data_binary
            else:  
                command = opcode + file1_length_binary + file_name_binary

            socket.send(command.encode())

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

    # Receive response from server
