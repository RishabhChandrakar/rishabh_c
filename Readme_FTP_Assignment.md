Features
User Authentication: Users are required to authenticate themselves with a username and password before accessing the server functionalities.

User Administration: Administrators have additional privileges to manage users, including adding, deleting, banning, and unbanning users.

File Transfer: Authenticated users can list available files on the server, retrieve files from the server (RETR), and upload files to the server (STOR).

Prerequisites
Ensure you have Python installed on your system. This code is compatible with Python 3.

Usage
Server Setup: Modify the hostname and port variables in the code to match your server's hostname and desired port.

User Management: Users and their passwords are stored in a CSV file named user_file.csv. You can manually add users to this file before running the server. Each row represents a user, with the format: username,password,is_banned.

File Listing: The server maintains a list of available files in a CSV file named directory_files_list.csv. You can populate this file with the names of files available for transfer.

Running the Server: Execute the Python script to start the FTP server. It will listen for incoming connections on the specified port.

Connecting Clients: Clients can connect to the server using FTP client software or custom scripts. Upon connection, clients will be prompted to authenticate.

User Commands:

USER <username>: Authenticate with a username.
PASS <password>: Provide the password corresponding to the username.
LIST: List available files on the server.
RETR <filename>: Retrieve a file from the server.
STOR <filename>: Upload a file to the server.
Admin Commands (accessible only to users with admin privileges):

ADDUSER <username> <password>: Add a new user to the server.
DELUSER <username>: Delete an existing user from the server.
BANUSER <username>: Ban a user from accessing the server.
UNBANUSER <username>: Remove the ban from a user.
Exiting: To stop the server, send the QUIT command.
