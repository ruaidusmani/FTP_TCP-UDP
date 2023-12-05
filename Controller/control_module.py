import os

class controller:
    @staticmethod
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

        return str(opcode)

    @staticmethod
    def get_file_length(file_name):
        file_length = len(file_name) + 1

        #convert file length to string of 5 bits if it is less than 32
        if (file_length < 32):
            file_length_binary = format(file_length, '05b') 
        else:
            file_length_binary = -1  # else -1 because it is too long
        return str(file_length_binary)

    @staticmethod
    def get_file_name_binary(file_name):
        binary_string = ''.join(format(ord(char), '08b') for char in file_name)
        return str(binary_string)

    @staticmethod
    def get_file_size_binary(file):
        if not os.path.isfile(file):
            return -1
        file_size = os.path.getsize(file) # get file size in bytes
        file_size_binary = format(file_size, '032b') # convert this to 32-bit (4 byte) binary
        return str(file_size_binary)

    @staticmethod
    def get_file_data_binary(file):
        if not os.path.isfile(file):
            return -1
        with open(file, 'r') as f: # open file in binary mode
            file_data = f.read() # read file data

        file_data_binary = ""
        for i in range(0, len(file_data)):
            # convert each character to binary
            file_data_binary += format(ord(file_data[i]), '08b')

        return str(file_data_binary)

    @staticmethod
    def string_to_binary(string):
        binary_string = ''.join(format(ord(char), '08b') for char in string)
        return str(binary_string)

    @staticmethod
    def binary_to_string(binary_string):
        # Convert binary to string
        str_data = ''.join(chr(int(binary_string[i:i+8], 2)) for i in range(0, len(binary_string), 8))
        return str_data
