FTP Server

Overview
This FTP server implementation provides a basic yet functional FTP service with support for user authentication, file management, and administrative commands. The server is designed to handle multiple clients simultaneously while ensuring proper error handling.

Features
User Authentication: Users can authenticate using the USER <username> and PASS <password> commands.
File Management: Users can list files in the current directory (LIST), retrieve files from the server (RETR <filename>), and store files on the server (STOR <filename>).
Disconnect: Users can disconnect from the server using the QUIT command.
Error Handling: The server provides appropriate error messages for various scenarios, such as attempting to retrieve a nonexistent file or storing a file that already exists.
Admin Commands: Administrative commands allow an admin account to manage users, including adding, deleting, banning, and unbanning users.
Admin Commands
ADDUSER <username> <password>: Adds a new user to the server.
DELUSER <username>: Deletes a user from the server.
BAN <username>: Bans a user from accessing the server.
UNBAN <username>: Unbans a previously banned user.
Usage
Starting the Server: Run the FTP server script 

php
Copy code
python ftp_server.py <
Connecting Clients: Clients can connect to the server using any FTP client software or the provided FTP client script.

Executing Commands: Clients can execute various commands supported by the server, such as USER, PASS, LIST, RETR, STOR, and QUIT.

Admin Commands: Admins can use the provided admin commands to manage users on the server.

FTP Client

Overview
This FTP client script provides a simple command-line interface for interacting with an FTP server implementing the specified commands. Users can connect to the server, authenticate, and execute commands to manage files and directories.

Features
Connectivity: Users can connect to an FTP server using the specified hostname and port.
User Authentication: Users can authenticate with a username and password.
Command Execution: Users can execute commands such as LIST, RETR <filename>, STOR <filename>, and QUIT.
Error Handling: The client script handles errors gracefully, displaying appropriate messages for invalid commands or server responses.
Usage
Connecting to Server: Run the FTP client script


Copy code
python FTPclient.py 
Authentication: Enter your username and password when prompted to authenticate with the server.

Executing Commands: Enter commands at the prompt to perform actions such as listing files, downloading, uploading, or disconnecting from the server.

Exiting the Client: To exit the client, use the QUIT command or close the terminal window.
