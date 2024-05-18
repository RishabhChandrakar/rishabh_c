import socket
import csv



hostname="localhost"
port=9999
ftp_server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ftp_server.bind(("localhost",port))

ftp_server.listen(10)       # maximum clients

client,add=ftp_server.accept()


class client_class:

    def __init__(self,client_socket,add):

        self.user=False
        self.admin=False
        
        self.server_socket=client_socket
        self.add=add
        self.server_socket.send("I am the server accepted your connection request ".encode())
        self.files=files
        print("Connection from:", self.add)

        self.COMMANDS()
        
        
    def USER(self):

        message=self.server_socket.recv(1024).decode()
        username ,*passl=message.strip().split(maxsplit=1)
        print(username,passl[0])
        
        if not(self.check_user_existence(username)):

            self.server_socket.send(("Sorry "+str(username)+" does not exist").encode())

        else:

            self.PASS(passl[0],username)


    def PASS(self,password,username):

        

        if self.check_user_password(username,password):

            self.user=True
            
            if username=="admin":
                self.admin=True
                self.server_socket.send("admin".encode())
            else:
                self.server_socket.send("user".encode())
        else:

            self.server_socket.send("Sorry Incorrect Password ".encode())

    def updating_user_file(self,username,password):
    
        with open("user_file.csv","a") as csvfile:
            csvwriter=csv.writer(csvfile)
            csvwriter.writerow([username,password,False])              # third field is whether user is ban or not
            self.server_socket.send(str(username +" is added now ").encode())
            
    def check_user_existence(self,username):
        with open("user_file.csv","r") as csvfile:
            csvreader=csv.reader(csvfile)
            exist=False
            
            for row in csvreader:
                if row==[]:
                    continue
                elif username==row[0]:
                    exist=True
                    break
            return exist

    def check_user_password(self,username,password):

        with open("user_file.csv","r") as csvfile:
            csvreader=csv.reader(csvfile)
            
            for row in csvreader:
                if username==row[0]:
                    if password==row[1]:
                        return True
                    else:
                        break
            return False

    def check_banned(self,username):

        with open("user_file.csv","r") as csvfile:
            csvreader=csv.reader(csvfile)
            
            for row in csvreader:
                if username==row[0]:
                    return row[2]
                
                    

    def updating_directory_files_list(self,filename):

        with open("directory_files_list.csv","a") as csvfile:
            csvwriter=csv.writer(csvfile)
            csvwriter.writerow([filename])

    def list_files(self):
        with open("directory_files_list.csv","r") as csvfile:
            csvreader=csv.reader(csvfile)
            list_of_files=[]
            for row in csvreader:
                print(row)
                list_of_files.append(row)
            return list_of_files
                
        
           

    def COMMANDS(self):

        

        while True:
            
            command , *arg=self.server_socket.recv(1024).decode().strip().split(maxsplit=1)
            print(command)
            if command.upper()=="QUIT":
                
                print("Disconnected from ",self.add)
                self.server_socket.close()
                break

            elif command.upper()=="USER":
                print(command)
                self.USER()

                
                
            elif command.upper()=="LIST" and self.user==True:

                listoffiles=str(self.list_files())
                print(listoffiles)
            
                self.server_socket.send(listoffiles.encode())

            elif command.upper()=="RETR" and self.user==True:
                filename=arg[0]

                if filename in self.files:
                    self.send_file(filename)
                    self.server_socket.send("file sended".encode())
                else:
                    self.server_socket.send("not available".encode())
                    
            elif command.upper()=="STOR" and self.user==True:

                filename=arg[0]
                print(filename)

                self.recv_file(filename)

            # Admin user commands

            elif command.upper()=="ADDUSER" and self.admin:            # admin is already user

                authntict_msg=arg[0]
                print(authntict_msg)
                
                username, *passl=authntict_msg.strip().split(maxsplit=1)
                password=passl[0]
                
                self.ADDUSER(username,password)

            elif command.upper()=="DELUSER" and self.admin:

                username=arg[0]

                self.DELUSER(username)

            elif command.upper()=="BANUSER" and self.admin:
                username=arg[0]

                self.BANUSER(username)
                
            elif command.upper()=="UNBANUSER" and self.admin:
                username=arg[0]

                self.UNBANUSER(username)

    def send_file(self,filename):
        print(filename)
        
        with open(filename, 'rb') as file:
            
            file_data = file.read()

     
        self.server_socket.sendall(len(file_data).to_bytes(4, byteorder='big'))
       
        self.server_socket.sendall(file_data)

    def recv_file(self,filename):

        file_size_bytes =self.server_socket.recv(4)
        file_size = int.from_bytes(file_size_bytes, byteorder='big')
      
        
        # Receive the file data
        file_data = b''
        while len(file_data) < file_size:
            chunk = self.server_socket.recv(file_size - len(file_data))
            
            if not chunk:
                break
            file_data += chunk
        

        # Save the received file data to a file
        
        with open(filename , 'wb') as file:
            file.write(file_data)
     
        self.updating_directory_files_list(filename)

    def ADDUSER(self,username,password):

        if self.check_user_existence(username):

            self.server_socket.send(str(username+" already exist in server ").encode())
        else:

            self.updating_user_file(username,password)
        
        

    def DELUSER(self,username):

        if self.check_user_existence(username):

            
            with open("user_file.csv", 'r', newline='') as file:
                reader = csv.reader(file)
                row_index=0
                print(reader)
                
                for row in reader:
                    print(row)

                    if row==[]:
                        row_index+=1

                    elif row[0]==username:
                        break
                    else:
                        row_index+=1
            
            # Read the CSV file and store its contents in a list
            with open("user_file.csv", 'r', newline='') as file:
                reader = csv.reader(file)
                rows = list(reader)

           

            # Delete the specified row
            del rows[row_index]

            # Write the modified data back to the CSV file
            with open("user_file.csv", 'w', newline='') as file:
                writer = csv.writer(file)
                for row in rows:
                    if row!=[]:
                        writer.writerows([row])
                
            self.server_socket.send((str(username + " deleted from the server ")).encode())
            
        else:
            self.server_socket.send(str(username +" does not exist in server ").encode())
        
    def BANUSER(self,username):

        
        if not(self.check_user_existence(username)):
            self.server_socket.send(str(username+" doesn't exist").encode())
            
            
        elif self.check_banned(username)=="True":
         
            self.server_socket.send(str(username+" is already banned").encode())
            
        else:
            self.on_banning(username,True)    
            self.server_socket.send(str(username +" is now banned").encode())
            
    def UNBANUSER(self,username):

        if not(self.check_user_existence(username)):
            self.server_socket.send(str(username+" doesn't exist").encode())
            
        elif self.check_banned(username)=="False":
            self.server_socket.send(str(username +" is already unbanned ").encode())
            
        else:
            self.on_banning(username,False)
            self.server_socket.send(str(username+ " is now unbanned ").encode())

    def on_banning(self,username,TorF):
    
        with open("user_file.csv", 'r', newline='') as file:
            reader = csv.reader(file)
            row_index=0
            for row in reader:

                if row[0]==username:
                    break
                else:
                    row_index+=1

                    
            
            
        with open("user_file.csv", 'r', newline='') as file:
            reader = csv.reader(file)
            rows = list(reader)
            rows[row_index][2]=TorF

           
        with open("user_file.csv", 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(rows)
            
         
           

obj=client_class(client,add)

            



        
        
        
  
            
            
            

        

        
        
        
        
        
