import socket
import os

# Constants
BUFFER_SIZE = 1024
hostname,port = 'localhost', 21
USERS = {'admin': 'admin123', 'user1': 'password1', 'user2': 'password2'}
ADMIN_USERNAME = 'admin'
BANNED_USERS = set()

# FTP Commands
FTP_COMMANDS = {
    'USER': 'USER',
    'PASS': 'PASS',
    'LIST': 'LIST',
    'RETR': 'RETR',
    'STOR': 'STOR',
    'QUIT': 'QUIT',
    'ADDUSER': 'ADDUSER',
    'DELUSER': 'DELUSER',
    'BAN': 'BAN',
    'UNBAN': 'UNBAN'
}

# Functions
def handle_user_command(command, username):
    if command == 'USER':
        if username in USERS:
            return '331 User name okay, need password for authentication.'
        else:
            return '530 Not logged in, username invalid.'
    elif command == 'PASS':
        if USERS.get(username) == password:
            return '230 User logged in, proceed.'
        else:
            return '530 Not logged in, password incorrect.'
    else:
        return '500 Syntax error, command unrecognized.'

def list_files():
    files = os.listdir('.')
    return '\n'.join(files)

def retrieve_file(filename):
    if os.path.exists(filename):
        with open(filename, 'rb') as file:
            return file.read()
    else:
        return '550 File not found.'

def store_file(filename, data):
    if os.path.exists(filename):
        return '550 File already exists.'
    else:
        with open(filename, 'wb') as file:
            file.write(data)
        return '250 File transfer successful.'

def add_user(username, password):
    if username in USERS:
        return '550 User already exists.'
    else:
        USERS[username] = password
        return '250 User added successfully.'

def del_user(username):
    if username in USERS:
        del USERS[username]
        return '250 User deleted successfully.'
    else:
        return '550 User does not exist.'

def ban_user(username):
    if username in USERS and username != ADMIN_USERNAME:
        BANNED_USERS.add(username)
        return '250 User banned successfully.'
    else:
        return '550 User cannot be banned.'

def unban_user(username):
    if username in BANNED_USERS:
        BANNED_USERS.remove(username)
        return '250 User unbanned successfully.'
    else:
        return '550 User is not banned.'

def handle_command(command, args, username):
    if username in BANNED_USERS:
        return '530 User is banned.'

    if command in ['USER', 'PASS']:
        return handle_user_command(command, args)
    elif command == 'LIST':
        return list_files()
    elif command == 'RETR':
        return retrieve_file(args)
    elif command == 'STOR':
        filename, data = args.split(maxsplit=1)
        return store_file(filename, data.encode())
    elif command == 'ADDUSER':
        username, password = args.split(maxsplit=1)
        return add_user(username, password)
    elif command == 'DELUSER':
        return del_user(args)
    elif command == 'BAN':
        return ban_user(args)
    elif command == 'UNBAN':
        return unban_user(args)
    else:
        return '500 Syntax error in parameters or arguments.'

def main():

        server_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((hostname,port))
        server_socket.listen(5)
                           
        print("FTP Server listening on ",hostname," : ",port)

        while True:
            client_socket, client_address = server_socket.accept()
            print("Connection from:", client_address)

            with client_socket:
                username = None
                while True:
                    data = client_socket.recv(1024)
                    if not data:
                        break
                    command, *args = data.decode().strip().split(maxsplit=1)
                    command = command.upper()

                    if command == 'QUIT':
                        client_socket.sendall(b'221 Goodbye.\n')
                        break

                    response = handle_command(command, *args, username)
                    client_socket.sendall(response.encode() + b'\n')

                    if command == 'USER' and response.startswith('331'):
                        username = args[0]

            print("Disconnected from:", client_address)

if __name__ == "__main__":
    main()
