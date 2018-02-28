import sys
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog, QPushButton, QLabel, QGridLayout, QFrame, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtCore import QDir
from fileparsing import parsing
import socket



class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 file dialogs - pythonspot.com'
        self.initUI()

    def initUI(self):
        #background image
        label = QLabel(self)
        pixmap = QPixmap('yellow-pastel-paint-texture-1638434-639x426.jpg')
        label.setPixmap(pixmap)
        self.resize(pixmap.width(), pixmap.height())
        
        
        #App components
        self.title = QLabel("<h1>Wafer Map Signature Tool</h1>", self)
        self.line = QLabel("<b>_______________________________________________________________________________________________________</b>", self)
        self.fileName = QLabel("<b>File Name: </b>", self)
        self.txtType = QLabel("<b>.txt files only</b>", self)
        self.fileNameBox = QLineEdit(self)
        self.fileNameBox.setReadOnly(True)
        self.fileNameBox.setFixedWidth(270)
        
        #Buttons Name
        self.inputButton = QPushButton("Browse", self)
        self.connectButton =  QPushButton("Print Report", self)
        self.uploadButton = QPushButton("Upload", self)
        
        #Title placement
        self.title.move(15,10)
        self.line.move(10, 30)
        
        #Components placement
        self.fileName.move(25, 80)
        self.fileNameBox.move(110, 80)
        self.inputButton.move(390, 75)
        self.txtType.move(110, 105)
        self.uploadButton.move(390, 100)
        self.connectButton.move(40, 300)
        
        #Buttons Action
        self.inputButton.clicked.connect(self.openFileNamesDialog)
        self.uploadButton.clicked.connect(self.uploadFunc)
        self.connectButton.clicked.connect(self.printReport)
        
        self.setFixedSize(pixmap.width(), pixmap.height())
        
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
        self.server_address = ('10.147.76.70', 10000)
        print (sys.stderr, 'connecting to %s port %s' % self.server_address)
        self.sock.connect(self.server_address)

    def printReport(self):
        self.sock.sendto("Send Report", self.server_address)

if __name__ == '__main__':
#    # Create a TCP/IP socket
#    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#
#    # Connect the socket to the port where the server is listening
#    server_address = ('10.145.220.247', 10000)
#    print (sys.stderr, 'connecting to %s port %s' % server_address)
#    sock.connect(server_address)

    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
