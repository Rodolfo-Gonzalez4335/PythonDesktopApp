import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog, QPushButton, QLabel, QGridLayout, QFrame, QHBoxLayout, QVBoxLayout, QTextEdit
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtCore import QDir, Qt
import socket
from datetime import datetime




class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 file dialogs - pythonspot.com'
        #Strings
        self.serverConnection = ""
        self.trained = ""
        self.outputReady = ""
        self.initUI()

    def initUI(self):
        #background image
        label = QLabel(self)
        pixmap = QPixmap('technology-background-1632715-1279x854.jpg')
        label.setPixmap(pixmap)
        self.resize(pixmap.width(), pixmap.height())


        #App components
        self.title = QLabel("<h1><font color='white'>\t\t\t Wafer Map Signature Tool</font></h1>", self)
        self.line = QLabel("<b><font color = 'white'>_______________________________________________________________________________________________________________________________________________________________________________________________________________</font></b>", self)
        self.fileName = QLabel("<b><font color='white'>File Name: </font></b>", self)
        self.txtType = QLabel("<b><font color='white'>.txt files only </font></b>", self)
        self.fileNameBox = QLineEdit(self)
        self.fileNameBox.setReadOnly(True)
        self.fileNameBox.setFixedWidth(300)
        
        self.consoleField = QTextEdit(self)
        self.consoleField.setReadOnly(True)
        self.consoleField.setFixedSize(690,150)

        #Buttons Name
        self.inputButton = QPushButton("Browse", self)
        self.printButton =  QPushButton("Print Report", self)
        self.uploadButton = QPushButton("Upload", self)
        self.trainButton = QPushButton("Train", self)
        self.connectButton = QPushButton("Check Connection", self)

        #Title placement
        self.title.move(15,10)
        self.line.move(10, 35)

        #Components placement
        self.fileName.move(25, 80)
        self.fileNameBox.move(120, 80)
        self.inputButton.move(430, 75)
        self.txtType.move(120, 110)
        self.uploadButton.move(430, 110)
        self.printButton.move(40, 300)
        self.trainButton.move(200, 300)
        self.connectButton.move(300, 300)
        self.consoleField.move(0, 426)
        

        #Buttons Action
        self.inputButton.clicked.connect(self.openFileNamesDialog)
        self.uploadButton.clicked.connect(self.uploadFunc)
        self.printButton.clicked.connect(self.printReport)
        self.trainButton.clicked.connect(self.trainMachine)
        self.connectButton.clicked.connect(self.checkConnection)

        self.setFixedSize(690, 526)

        #Layout
        self.consoleOutput()
        self.setWindowTitle("Senior Project Tool")
        self.show()


    def sendFilesToServer(self, fileName):
        f = open(fileName,'rb')
        while True:
            message = f.read(1024)
            if not message:
                f.close()
                break
            self.sock.sendto(message, self.server_address)

    def openFileNamesDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.filenames = QFileDialog.getOpenFileNames(self,"Upload Files", "","Text files (*.txt)", options=options)
        filename, _ = self.filenames
        if filename:
            self.fileNameBox.setText(str(filename))

    def uploadFunc(self):
        try:
            self.ConnectToServer()
            self.fileNameBox.setText("")
            f = open(str(self.filenames[0][0]), 'r')
            for i in range(0, len(self.filenames[0])):
                self.sendFilesToServer(self.filenames[0][i])
            self.outputReady = "Your files are ready to be printed"
            self.consoleOutput()
            self.DisconnectToServer()
        except:
            self.outputReady = "Your files failed to be uploaded"
            self.consoleOutput()


    def DisconnectToServer(self):
        self.sock.close()
        self.serverConnection = "You are now disconnected from the server"
        self.consoleOutput()

    def ConnectToServer(self):
        try:
            # Create a TCP/IP socket
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Connect the socket to the port where the server is listening
            # '10.147.76.70'
            self.server_address = ("10.145.235.30", 10000)
            self.sock.connect(self.server_address)
            self.serverConnection = "You are now connected to the server"
            self.consoleOutput()
        except:
            self.serverConnection = "Server is not connected"
            self.consoleOutput()


    def printReport(self):
        try:
            self.ConnectToServer()
            self.sock.sendto("Send Report".encode('utf-8'), self.server_address)
            dir_path = os.path.join(os.getcwd(), "Report_files")
            i = 1
            f=open(os.path.join(dir_path, 'received_file'+ str(i)+".txt"),'w')
            i=i+1
            while True:
                data = self.sock.recv(1024)
                data_decoded = data.decode()
                if not data:
                    f.close()
                    break
                if f.closed and data_decoded != "":
                    f=open(os.path.join(dir_path, 'received_file' + str(i)+".txt"), 'w')
                    i = i+1
                if "EOF" in data_decoded:
                    index_begin = 0
                    index_end = 0
                    separateFiles = []
                    for index in range(data_decoded.count("EOF")):
                        if index_end == 0:
                            index_end = data_decoded.find("EOF")
                        else:
                            index_begin=index_end+3
                            index_end = index_begin + data_decoded[index_begin:].find("EOF")

                        separateFiles.append(data_decoded[index_begin:index_end])
                
                    if index_end+3<len(data_decoded):
                        if data_decoded[index_end+2:].find("W")>-1:
                            index_begin =index_end+3
                            separateFiles.append(data_decoded[index_begin + data_decoded[index_end+3:].find("W") : ])
#                    print(separateFiles.count()
                    for index in range(len(separateFiles)):
                        if separateFiles[index] != "":
                            f.write(separateFiles[index])
                        if index != len(separateFiles)-1 and separateFiles[index] != "" and separateFiles[index].find("W") > -1:
                            f.close()
                            f=open(os.path.join(dir_path, 'received_file' + str(i)+".txt"), 'w')
                            i=i+1
                        elif separateFiles[index].find("W") != -1:
                            f.close()
                else:
                    f.write(data_decoded)
            self.outputReady = "Your report has been printed, go to GUI/Report_files"
            self.consoleOutput()
            self.DisconnectToServer()
        except:
            self.outputReady = "Printing failed"
            self.consoleOutput()
                

    def trainMachine(self):
        try:
            self.ConnectToServer()
            self.sock.sendto("Training mode".encode('utf-8'), self.server_address)
            data = self.sock.recv(1024)
            self.trained = str(data.decode())
            self.consoleOutput()
            self.DisconnectToServer()
        except:
            self.trained = "Training failed"
            self.consoleOutput()

    def isItTrained(self):
        try:
            self.ConnectToServer()
            self.sock.sendto("is it trained".encode('utf-8'), self.server_address)
            data = self.sock.recv(1024)
            if(data.decode() == "yes"):
                self.trained = "The machine has been trained"
            else:
                self.trained = "Machine has not been trained yet"
            self.consoleOutput()
        except:
            pass
                
    def checkConnection(self):
        try:
            self.isItTrained()
            self.serverConnection = "Server is working"
            self.consoleOutput()
            self.sock.close()
        except:
            pass

    def consoleOutput(self):
        self.consoleField.setText("Console: \n" + self.serverConnection + "\n" + self.trained + "\n" + self.outputReady)

if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
