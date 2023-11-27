import socket 

def get_opcode(command):
    command_breakdown = command.split()
    user_command = command_breakdown[0]
    opcode = ""

    if user_command == "put":
        opcode = "000"
    elif user_command == "get":
        opcode = "001"
    elif user_command == "summary":
        opcode = "010"
    elif user_command == "change":
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
    print("Connected")


# elif (protocol == "UDP"):
#     socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print("Session has been established.")

# print list of commands
#TODO: Implement this in the help command coming from the server
print ("Commands are: bye, change, get, help, put, summary")

# main loop
while True:
    # Ask user for command
    full_command = input("")
    command_array = full_command.split()

    # Check command validity
    if command_array[0] in ["help", "bye"]:
        if len(command_array) == 1:
            if command_array[0] == "bye":
                print("Session is terminated.")
                break
            elif command_array[0] == "help":
                opcode = get_opcode(command_array[0])
        else:
            print("Invalid command, please try again.")
            continue
    elif command_array[0] in ["put", "get", "summary"]:
        if len(command_array) == 2:
            opcode = get_opcode(command_array[0])
            file1_length_binary = get_file_length(command_array[1])
            if file1_length_binary == -1:
                print("File name is too long, please try again.")
                continue
        else:
            print("Invalid command, please try again.")
            continue
    elif command_array[0] == "change":
        if len(command_array) == 3:
            opcode = get_opcode(command_array[0])
            file1_length_binary = get_file_length(command_array[1])
            file2_length_binary = get_file_length(command_array[2])
            if file1_length_binary == -1 and file2_length_binary == -1:
                print("File name is too long, please try again.")
                continue
        else:
            print("Invalid command, please try again.")
            continue
    else:
        print("Invalid command, please try again.")
        continue

    # Send command to server
