import sys
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog, QPushButton, QHBoxLayout
from PyQt5.QtGui import QIcon
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
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.inputButton = QPushButton("Input Files")
        self.connectButton =  QPushButton("See Server Mappings")
        v_box = QHBoxLayout()
        v_box.addWidget(self.inputButton)
        v_box.addWidget(self.connectButton)

        self.setLayout(v_box)
        self.setWindowTitle("PyQt5")
        self.inputButton.clicked.connect(self.openFileNamesDialog)
        self.connectButton.clicked.connect(self.connectToServer)
        # self.openFileNameDialog()
        # self.openFileNamesDialog()
        # self.saveFileDialog()

        self.show()

    def sendFilesToServer(self, fileName):
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
        filenames = QFileDialog.getOpenFileNames(self,"Upload files", "","Text files (*.txt)", options=options)
        f = open(str(filenames[0][0]), 'r')
        for i in range(0, len(filenames[0])):
            self.sendFilesToServer(filenames[0][i])

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
