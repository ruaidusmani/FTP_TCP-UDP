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

def get_file_length(command):
    command_breakdown = command.split()
    file_name = command_breakdown[1]
    file_length = len(file_name) + 1

    return file_length

# Connect to server


# Ask user for decision on TCP or UDP
protocol_decision = input("Press 1 for TCP, Press 2 for UDP: ")
protocol = ""

if protocol_decision == "1":
    protocol = "TCP"
    pass

elif protocol_decision == "2":
    protocol = "UDP"
    pass

else:
    print("Invalid input, please try again.")

# Ask user for IP address and port number
ip_address, port_number = input("Provide IP address and Port Number: ").split()
ip_address = (ip_address)
port_number = int(port_number)

# print list of commands
print ("Commands are: bye, change, get, help, put, summary")

progress = True
while (progress):
    # Ask user for command
    command = input("")
    if command != "bye":
        opcode = get_opcode(command)
        FL = get_file_length(command)

    else:
        progress = False

print("Session is terminated.")

