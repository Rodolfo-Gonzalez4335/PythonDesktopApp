import sys
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog, QPushButton, QLabel, QGridLayout, QFrame, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtCore import QDir
from fileparsing import parsing
import socket
import sys

def DisconnectToServer():
    conn.close()

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 file dialogs - pythonspot.com'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()

    def initUI(self):
        
        label = QLabel(self)
        pixmap = QPixmap('yellow-pastel-paint-texture-1638434-639x426.jpg')
        label.setPixmap(pixmap)
        self.resize(pixmap.width(), pixmap.height())
        
        
        grid = QGridLayout()
        hbox = QHBoxLayout()
        hbox1 = QHBoxLayout()
        hbox2 = QHBoxLayout()
        hbox3 = QHBoxLayout()
        vbox = QVBoxLayout()
        #self.setGeometry(self.left, self.top, self.width, self.height)
        
        self.title = QLabel("<h1>Wafer Map Signature Tool</h1>", self)
        self.line = QLabel("<b>_______________________________________________________________________________________________</b>", self)
        self.fileName = QLabel("<b>File Name: </b>", self)
        self.txtType = QLabel("<b>.txt files only</b>", self)
        self.fileNameBox = QLineEdit(self)
        self.fileNameBox.setReadOnly(True)
        self.fileNameBox.setFixedWidth(200)
        
        
        
#        hbox.addWidget(title)
#        hbox1.addWidget(self.HLine())
#        hbox2.addWidget(fileName)
#        hbox2.addWidget(fileNameBox)
#        

        self.inputButton = QPushButton("Browse", self)
        #self.connectButton =  QPushButton("See Server Mappings", self)
        self.uploadButton = QPushButton("Upload", self)
        
#        hbox2.addWidget(self.inputButton)
#        hbox3.addWidget(blank)
#        hbox3.addWidget(txtType)
#        hbox3.addWidget(self.uploadButton)
#        
#        vbox.addLayout(hbox)
#        vbox.addLayout(hbox1)
#        vbox.addLayout(hbox2)
#        vbox.addLayout(hbox3)

        self.title.move(15,10)
        self.line.move(10, 25)
        
        self.fileName.move(25, 80)
        self.fileNameBox.move(110, 80)
        self.inputButton.move(320, 75)
        self.txtType.move(110, 105)
        self.uploadButton.move(320, 100)
        

#self.setLayout(vbox)
        self.setWindowTitle("Senior Project Tool")
        self.inputButton.clicked.connect(self.openFileNamesDialog)
        self.uploadButton.clicked.connect(self.uploadFunc)
        #self.connectButton.clicked.connect(self.connectToServer)
        
        #self.saveFileDialog()
        #self.setFixedSize(570, 400)
        self.show()
    
    def HLine(self):
        toto = QFrame()
        toto.setFrameShape(QFrame.HLine)
        toto.setFrameShadow(QFrame.Sunken)
        return toto

    def sendFilesToServer(self, fileName):
        self.fileNameBox.setText("")
        try:
            # Send data
            f = open(fileName,'rb')
            while True:
                message = f.read(1024)
                if not message:
                    break
                print (sys.stderr, 'sending "%s"\n' % message)
                sock.sendto(message,server_address)
        except:
            print("There was an problem sending the file data.\n")
        try:
            f = open('datareceived.txt', 'w')
            amount_received = 0
            amount_expected = 9000
            while amount_received < amount_expected:
                data = sock.recv(9000)
                f.write(data.decode('utf-8'))
                f.close()
                amount_received += len(data)
                print (sys.stderr, 'received %s' % data)
        except:
            print("There was a problem sending the file data.")

    def openFileNamesDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.filenames = QFileDialog.getOpenFileNames(self,"Upload Files", "","Text files (*.txt)", options=options)
        filename, _ = self.filenames
        self.fileNameBox.setText(str(filename))
#        f = open(str(filenames[0][0]), 'r')
#        for i in range(0, len(filenames[0])):
#            self.sendFilesToServer(filenames[0][i])

    def uploadFunc(self):
        f = open(str(self.filenames[0][0]), 'r')
        for i in range(0, len(self.filenames[0])):
            self.sendFilesToServer(self.filenames[0][i])

    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()","","All Files (*);;Text Files (*.txt)", options=options)
        if fileName:
            print(fileName)

    def connectToServer(self):
        print ("Create Window")
        #try:
        #look for response
        #    amount_received = 0
        #    amount_expected = len(message)
        #
        #    while amount_received < amount_expected:
        #        data = sock.recv(16)
        #        amount_received += len(data)
        #        print(sys.stderr, 'received %s' % message)
        #except:
        #    print ("There was a problem receiving the file data.")

if __name__ == '__main__':
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    server_address = ('localhost', 10000)
    print (sys.stderr, 'connecting to %s port %s' % server_address)
    sock.connect(server_address)

    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
