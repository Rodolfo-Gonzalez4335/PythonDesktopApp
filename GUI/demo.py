import sys
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog, QPushButton, QHBoxLayout
from PyQt5.QtGui import QIcon
from fileparsing import parsing
#import pymysql.cursors
#import socket
#import mysql.connector




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

    def openFileNamesDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filenames = QFileDialog.getOpenFileNames(self,"Upload files", "","Text files (*.txt)", options=options)
        f = open(str(filenames[0][0]), 'r')
        for i in range(0, len(filenames[0])):
            print(filenames[0][i])
            
    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()","","All Files (*);;Text Files (*.txt)", options=options)
        if fileName:
            print(fileName)

    def connectToServer(self):
        print ("Create Window")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
