import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog, QPushButton, QLabel, QGridLayout, QFrame, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtCore import QDir, Qt
#from fileparsing import parsing
import socket



class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 file dialogs - pythonspot.com'
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

        #Buttons Name
        self.inputButton = QPushButton("Browse", self)
        self.connectButton =  QPushButton("Print Report", self)
        self.uploadButton = QPushButton("Upload", self)
        self.trainButton = QPushButton("Train", self)

        #Title placement
        self.title.move(15,10)
        self.line.move(10, 35)

        #Components placement
        self.fileName.move(25, 80)
        self.fileNameBox.move(120, 80)
        self.inputButton.move(430, 75)
        self.txtType.move(120, 110)
        self.uploadButton.move(430, 110)
        self.connectButton.move(40, 300)
        self.trainButton.move(200, 300)

        #Buttons Action
        self.inputButton.clicked.connect(self.openFileNamesDialog)
        self.uploadButton.clicked.connect(self.uploadFunc)
        self.connectButton.clicked.connect(self.printReport)
        self.trainButton.clicked.connect(self.trainMachine)

        self.setFixedSize(639, 426)

        #Layout
        self.setWindowTitle("Senior Project Tool")
        self.show()


    def sendFilesToServer(self, fileName):
        try:
            # Send data
            print ("------------------"+"\n\n\n"+fileName)
            f = open(fileName,'rb')
            while True:
                message = f.read(1024)
                if not message:
                    f.close()
                    break
                print (sys.stderr, 'sending "%s"\n' % message.decode())
                self.sock.sendto(message, self.server_address)
        except:
            print("There was a problem sending the file data.\n")

    def openFileNamesDialog(self):
#        self.ConnectToServer()
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.filenames = QFileDialog.getOpenFileNames(self,"Upload Files", "","Text files (*.txt)", options=options)
        filename, _ = self.filenames
        if filename:
            self.fileNameBox.setText(str(filename))

    def uploadFunc(self):
        self.ConnectToServer()
        self.fileNameBox.setText("")
        f = open(str(self.filenames[0][0]), 'r')
        for i in range(0, len(self.filenames[0])):
            self.sendFilesToServer(self.filenames[0][i])
        self.DisconnectToServer()


    def DisconnectToServer(self):
        self.sock.close()

    def ConnectToServer(self):
        # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect the socket to the port where the server is listening
        # '10.147.76.70'
        self.server_address = ("localhost", 10000)
        print (sys.stderr, 'connecting to %s port %s' % self.server_address)
        self.sock.connect(self.server_address)

    def printReport(self):
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
                separateFile = data_decoded.split("EOF")
                f.write(separateFile[0])
                f.close()
            else:
                f.write(data_decoded)
        self.DisconnectToServer()

    def trainMachine(self):
        self.ConnectToServer()
        self.sock.sendto("Training mode".encode('utf-8'), self.server_address)
#        self.fileNameBox.setText("")
#        f = open(str(self.filenames[0][0]), 'r')
#        for i in range(0, len(self.filenames[0])):
#            sendFilesToServer(self.filenames[0][i])
        data = self.sock.recv(1024)
        print(data.decode())
        self.DisconnectToServer()

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
