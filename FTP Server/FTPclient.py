import socket

class FTPClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.socket.connect((self.host, self.port))
        print("Connected to FTP server.")

    def send_command(self, command):
        self.socket.sendall(command.encode())
       
        response = self.socket.recv(4096).decode()
        print(response)

    def login(self, username, password):
        self.send_command(f"USER {username}\n")
        self.send_command(f"PASS {password}\n")

    def list_files(self):
        self.send_command("LIST\n")

    def download_file(self, filename):
        self.send_command(f"RETR {filename}\n")

    def upload_file(self, filename):
        self.send_command(f"STOR {filename}\n")

    def quit(self):
        self.send_command("QUIT\n")
        self.socket.close()
        print("Disconnected from FTP server.")

def main():
    host = 'localhost'
    ftp_client = FTPClient(host, port)
    ftp_client.connect()

    # Login
    username = input("Enter username: ")
    password = input("Enter password: ")
    ftp_client.login(username, password)

    while True:
        command = input("Enter command (LIST, RETR <filename>, STOR <filename>, QUIT): ").strip()
        if command.upper() == 'QUIT':
            ftp_client.quit()
            break
        elif command.upper().startswith('RETR'):
            filename = command.split()[1]
            ftp_client.download_file(filename)
        elif command.upper().startswith('STOR'):
            filename = command.split()[1]
            ftp_client.upload_file(filename)
        elif command.upper() == 'LIST':
            ftp_client.list_files()
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()
