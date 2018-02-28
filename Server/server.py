import socket
from socket import gethostbyname
import sys
from fileparsing import fileparsing


class Server:
    def __init__(self):
        self.host = gethostbyname( '0.0.0.0' )
        self.server_address = (self.host, 10000)
        # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(self.server_address)
        self.sock.listen(1)
        print (sys.stderr, 'starting up on %s port %s' % self.server_address)

    def readCommands(self):
        while True:
            # Wait for a connection
            print ('waiting for a connection')
            connection, client_address = self.sock.accept()
            print (sys.stderr, 'connection from', client_address)

            try:
                i=1
                f=open('file_'+ str(i)+".txt",'w')
                i= i+1
                # Receive the data in small chunks and retransmit it
                while True:
                    data = connection.recv(1024)
                    data_decoded = data.decode()
                    if "Send Report" in data_decoded:
                        connection.sendall("Meny is cool NOT".encode('utf-8'))
                    else:
                        print (sys.stderr, 'received "%s"' % data_decoded)
                        if not data:
                            print (sys.stderr, 'empty data from client', client_address)
                            f.close();
                            # idk = fileparsing("file_"+str(i))
                            # idk.parse();
                            break
                        if f.closed and data_decoded!="":
                            print ("!!!!!!!!f.close"+ data_decoded)
                            f=open('file_'+ str(i)+".txt",'w')
                            i= i+1
                        if "EndOfFile" in data_decoded:
                            idk = data_decoded.split("EndOfFile;")
                            f.write(idk[0])
                            f.close();
                            if len(idk)==2:
                                if idk[1] and data_decoded!="":
                                    print ("~~~~~~~~~~"+idk[1]+"~~~~~~~~~~")
                                    f=open('file_'+ str(i)+".txt",'w')
                                    i= i+1
                                    f.write(idk[1])
                        else:
                            f.write(data_decoded)


                        # if data:
                            # print (sys.stderr, 'sending data back to the client')
                            # connection.sendall(data)
                        # else:


            finally:
                # Clean up the connection
                connection.close()

server = Server();
server.readCommands();
