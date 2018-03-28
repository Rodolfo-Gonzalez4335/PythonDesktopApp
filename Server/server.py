import socket
from socket import gethostbyname
import sys
from fileparsing import fileparsing
import os
import numpy as np
import sys
import matplotlib.pyplot as plt


class Server:
    def __init__(self):
        self.host = gethostbyname( '0.0.0.0' )
        #self.host 10.145.31.19
        self.server_address = (self.host, 10000)
        # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(self.server_address)
        self.sock.listen(1)
        print (sys.stderr, 'starting up on %s port %s' % self.server_address)
    def column(self,matrix, i):
        return [row[i] for row in matrix]

    def plotFile(self,file_path):
        file = open(file_path,"r")
        for line in file:
            if 'DefectList' in line:
                array_of_nums = []
                for line in file:
                    if 'SummarySpec' in line:
                        break
                    nums = []
                    for num in line.strip(' ').split(' '):
                        try:
                            nums.append(float(num))
                        except ValueError:
                            if num!="":
                                num = num.replace(';','')
                                nums.append(float(num))
                                pass
                    array_of_nums.append(nums)
                continue
        file.close()
        x_offs = np.array(self.column(array_of_nums,3))
        y_offs = np.array(self.column(array_of_nums,4))
        x_locs = np.array(self.column(array_of_nums,1))
        y_locs = np.array(self.column(array_of_nums,2))
        x = np.add(x_locs, 1000*x_offs)
        y = np.add(y_locs, 1000*y_offs)
        # Plot a scatter plot
        plt.figure(figsize=(8, 6))
        plt.scatter(x,y)
        frame1 = plt.gca()
        frame1.axes.xaxis.set_ticklabels([])
        frame1.axes.yaxis.set_ticklabels([])
        plot_name = "classified_images/classified.png"
        plt.savefig(plot_name)
        plt.close()
        return plot_name

    def readCommands(self):
        while True:
            # Wait for a connection
            print ('waiting for a connection')
            connection, client_address = self.sock.accept()
            print (sys.stderr, 'connection from', client_address)

            try:
                i=1
                # Open file to input_files directory in Server
                dir_path = os.path.join(os.getcwd(), "input_files")
                f=open(os.path.join(dir_path, 'file_'+ str(i)+".txt"),'w')
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
                            file = fileparsing()
                            file.parse();
                            break
                        if f.closed and data_decoded!="":
                            print ("!!!!!!!!f.close"+ data_decoded)
                            f=open(os.path.join(dir_path, 'file_'+ str(i)+".txt"),'w')
                            i= i+1
                        if "EndOfFile" in data_decoded:
                            idk = data_decoded.split("EndOfFile;")
                            f.write(idk[0])
                            f.close();
                            if len(idk)==2:
                                if idk[1] and data_decoded!="":
                                    print ("~~~~~~~~~~"+idk[1]+"~~~~~~~~~~")
                                    f=open(os.path.join(dir_path, 'file_'+ str(i)+".txt"),'w')
                                    i= i+1
                                    f.write(idk[1])
                        else:
                            f.write(data_decoded)


            finally:
                connection.close()
                for filename in os.listdir(dir_path):
                    if filename.endswith(".txt") :
                        self.plotFile(dir_path+"/" + filename)
                        continue
                    else:
                        continue
server = Server();
server.readCommands();
