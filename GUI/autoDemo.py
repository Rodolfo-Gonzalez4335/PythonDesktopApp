import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog, QPushButton, QLabel, QGridLayout, QFrame, QHBoxLayout, QVBoxLayout, QTextEdit, QComboBox, QStyleFactory, QMessageBox
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtCore import QDir, Qt, QLine
import socket
import time
import numpy as np
import matplotlib.pyplot as plt




class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 file dialogs - pythonspot.com'
        #Strings
        self.serverConnection = ""
        self.trained = ""
        self.outputReady = ""
        self.hasCorrected = ""
        
        self.x = 0
        self.y = 0
        self.z = 0
        
        screen_resolution = app.desktop().screenGeometry()
        width, height = screen_resolution.width(), screen_resolution.height()
        
        
        if sys.platform == "darwin":
            self.initUI()
        elif width < 2100 and height < 1500:
            self.x = 200
            self.y = 600
            self.z = 100
            self.windowsGui()
        else:
            self.windowsGui()

    def windowsGui(self):
        #background image
        label = QLabel(self)
#        pixmap = QPixmap('yellow-pastel-paint-texture-1638434.jpg')
#        label.setPixmap(pixmap)
#        self.resize(pixmap.width(), pixmap.height())

        ## show plot button attributes
        self.showPlotUpload = QPushButton("Show Plot", self)
        self.showPlotUpload.move(160, 145)
        self.showPlotUpload.clicked.connect(self.showPlotUploadFunc)
        
        #App components
        self.title = QLabel("<h1>\t\t\t Wafer Map Signature Classification Tool</h1>", self)
        self.line = QLabel("<b>_______________________________________________________________________________________________________________________________________________________________________________________________________________</b>", self)
        self.fileName = QLabel("<b>File Name: </b>", self)
        self.txtType = QLabel("<b>.txt files only </b>", self)
        self.correcTitle = QLabel("<h3>User Correction: </h3>", self)
        self.fileNameBox = QLineEdit(self)
        self.fileNameBox.setReadOnly(True)
        self.fileNameBox.setFixedWidth(800)
        
        self.verticalLine = self.verticalFuncWin()
        
        self.consoleField = QTextEdit(self)
        self.consoleField.setReadOnly(True)
        self.consoleField.setFixedSize(2100-self.x,300-self.z)
        
        self.comboBox = QComboBox(self)
        self.comboBox.addItems(["Edge", "Electrode", "Hotspot", "Large Edge", "Probe Marks", "Repeater", "Ring", "Scratch", "Slides", "Spin", "Spray", "Streak"])
        
        
        #Buttons Name
        self.inputButton = QPushButton("Browse", self)
        self.printButton =  QPushButton("Print Reports", self)
        self.uploadButton = QPushButton("Upload", self)
        self.trainButton = QPushButton("Train", self)
        self.connectButton = QPushButton("Check Connection", self)
        self.userCorrect = QPushButton("Correction", self)
        self.helpButton = QPushButton("Help", self)
        
        #Title placement
        self.title.move(15,10)
        self.line.move(10, 35)
        
        #Components placement
        self.fileName.move(25, 80)
        self.fileNameBox.move(160, 80)
        self.inputButton.move(975, 75)
        self.txtType.move(160, 110)
        self.uploadButton.move(975, 145)
        self.printButton.move(160, 600-self.z)
        self.trainButton.move(360, 600-self.z)
        self.connectButton.move(560, 600-self.z)
        self.consoleField.move(0, 1200-self.y)
        self.correcTitle.move(1450-(self.z), 60)
        self.comboBox.move(1450-(self.z), 120)
        self.userCorrect.move(1450-(self.z), 180)
        self.helpButton.move(1450-(self.z), 300)
        
        
        #Buttons Action
        self.inputButton.clicked.connect(self.openFileNamesDialog)
        self.uploadButton.clicked.connect(self.uploadFunc)
        self.printButton.clicked.connect(self.printReport)
        self.trainButton.clicked.connect(self.trainMachine)
        self.connectButton.clicked.connect(self.checkConnection)
        self.userCorrect.clicked.connect(self.uCorrection)
        self.helpButton.clicked.connect(self.helpFunct)
        
        #window size
        self.setFixedSize(2100-self.x, 1500-self.y)
        
        
        #Layout
        self.consoleOutput()
        self.setWindowTitle("Senior Project Tool")
        self.show()

    def initUI(self):
        #background image
        label = QLabel(self)
#        pixmap = QPixmap('yellow-pastel-paint-texture-1638434-1599x1066.jpg')
#        label.setPixmap(pixmap)
#        self.resize(pixmap.width(), pixmap.height())

        ## show plot button attributes
        self.showPlotUpload = QPushButton("Show Plot", self)
        self.showPlotUpload.move(200, 145)
        self.showPlotUpload.clicked.connect(self.showPlotUploadFunc)

        #App components
        self.title = QLabel("<h1>\t\t\t Wafer Map Signature Classification Tool</h1>", self)
        self.line = QLabel("<b>____________________________________________________________________________________________________________________________________________________________________________________________________________________</b>", self)
        self.fileName = QLabel("<b>File Name: </b>", self)
        self.txtType = QLabel("<b>.txt files only </b>", self)
        self.correcTitle = QLabel("<h3>User Correction: </h3>", self)
        self.fileNameBox = QLineEdit(self)
        self.fileNameBox.setReadOnly(True)
        self.fileNameBox.setFixedWidth(300)

        self.verticalFSFunc()

        self.consoleField = QTextEdit(self)
        self.consoleField.setReadOnly(True)
        self.consoleField.setFixedSize(820,150)

        self.comboBox = QComboBox(self)
        self.comboBox.addItems(["Edge", "Electrode", "Hotspot", "Large Edge", "Probe Marks", "Repeater", "Ring", "Scratch", "Slides", "Spin", "Spray", "Streak"])


        #Buttons Name
        self.inputButton = QPushButton("Browse", self)
        self.printButton =  QPushButton("Print Reports", self)
        self.uploadButton = QPushButton("Upload", self)
        self.trainButton = QPushButton("Train", self)
        self.connectButton = QPushButton("Check Connection", self)
        self.userCorrect = QPushButton("Correction", self)
        self.helpButton = QPushButton("Help", self)

        #Title placement
        self.title.move(15,10)
        self.line.move(10, 35)

        #Components placement
        self.fileName.move(25, 80)
        self.fileNameBox.move(120, 80)
        self.inputButton.move(430, 75)
        self.txtType.move(120, 110)
        self.uploadButton.move(300, 145)
        self.printButton.move(40, 300)
        self.trainButton.move(200, 300)
        self.connectButton.move(300, 300)
        self.consoleField.move(0, 450)
        self.correcTitle.move(620, 60)
        self.comboBox.move(630, 120)
        self.userCorrect.move(630, 150)
        self.helpButton.move(630, 250)


        #Buttons Action
        self.inputButton.clicked.connect(self.openFileNamesDialog)
        self.uploadButton.clicked.connect(self.uploadFunc)
        self.printButton.clicked.connect(self.printReport)
        self.trainButton.clicked.connect(self.trainMachine)
        self.connectButton.clicked.connect(self.checkConnection)
        self.userCorrect.clicked.connect(self.uCorrection)
        self.helpButton.clicked.connect(self.helpFunct)

        self.setFixedSize(820, 600)


        #Layout
        self.consoleOutput()
        self.setWindowTitle("Senior Project Tool")
        self.show()
    
    
    def showcaseUI(self):
        
        self.showPlotUpload.move(730, 75)
        self.fileNameBox.setFixedWidth(500)
        self.consoleField.setFixedSize(1280, 150)

        
        #Title placement
        self.title.move(15,10)
        self.line.move(10, 35)
        
        #Components placement
        self.fileName.move(25, 80)
        self.fileNameBox.move(120, 80)
        self.inputButton.move(630, 75)
        self.txtType.move(120, 110)
        self.uploadButton.move(630, 105)
        
        self.printButton.move(120, 350)
        self.trainButton.move(280, 350)
        self.connectButton.move(380, 350)
        
        self.consoleField.move(0, 650)
        self.correcTitle.move(970, 60)
        self.comboBox.move(990, 120)
        self.userCorrect.move(990, 150)
        self.helpButton.move(1100, 400)
        
        

        self.showFullScreen()
    
    
    def showNormal1(self):
        
        self.showPlotUpload.move(200, 145)
        self.fileNameBox.setFixedWidth(300)
        self.consoleField.setFixedSize(820,150)
        
        
        #Title placement
        self.title.move(15,10)
        self.line.move(10, 35)
        
        #Components placement
        self.fileName.move(25, 80)
        self.fileNameBox.move(120, 80)
        self.inputButton.move(430, 75)
        self.txtType.move(120, 110)
        self.uploadButton.move(300, 145)
        self.printButton.move(40, 300)
        self.trainButton.move(200, 300)
        self.connectButton.move(300, 300)
        self.consoleField.move(0, 450)
        self.correcTitle.move(620, 60)
        self.comboBox.move(630, 120)
        self.userCorrect.move(630, 150)
        self.helpButton.move(630, 250)
    
        self.showNormal()

        

    ## show plot functions

    def showPlotUploadFunc(self):
        if len(self.filenames[0]) > 1:
            self.outputReady = "Choose only one file to plot"
            self.consoleOutput()
        else:
            self.fileNameBox.setText("")
            f = open(str(self.filenames[0][0]), 'r')
            x = []
            y = []
            for line in f:
                if "DefectList" in line:
                    for line in f:
                        if "SummarySpec" in line:
                            break
                        linelist = line.strip(' ').split(' ')
                        x.append(float(linelist[1]) + (float(linelist[3])*1000))
                        y.append(float(linelist[2]) + (float(linelist[4])*1000))
            plt.figure(figsize = (7, 7))
            plt.scatter(x, y)
            frame1 = plt.gca()
            frame1.axes.xaxis.set_ticklabels([])
            frame1.axes.yaxis.set_ticklabels([])
            plt.xlabel("x")
            plt.ylabel("y")
            plt.show()

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
                time.sleep(0.1)
            print("got here")
            self.sock.sendall("END OF FILE SENDING".encode())
            self.outputReady = "Your files are being processed..."
            self.consoleOutput()
            self.ConnectToServer()
            data = self.sock.recv(1024)
            self.outputReady = (str(data.decode()))
            self.consoleOutput()
            self.DisconnectToServer()
        except Exception as e:
            print(e)
            self.outputReady = "Your files failed to be uploaded"
            self.consoleOutput()

    def VLine(self):
        toto = QFrame()
        toto.setFrameShape(QFrame.VLine)
        toto.setFrameShadow(QFrame.Sunken)
        return toto

    def DisconnectToServer(self):
        self.sock.close()

    def ConnectToServer(self):
        try:
            # Create a TCP/IP socket
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Connect the socket to the port where the server is listening
            self.server_address = ("10.145.117.235", 10000)
            #self.server_address = ("10.145.250.235", 10000)
            self.sock.connect(self.server_address)
            self.serverConnection = "You are now connected to the server"
            self.consoleOutput()
        #self.DisconnectToServer()
        except Exception as e:
            print(e)
            self.serverConnection = "Server is not connected"
            self.consoleOutput()

    def printReport(self):
        try:
            self.ConnectToServer()
            self.sock.sendto("Send Report".encode('utf-8'), self.server_address)
            dir_path = os.path.join(os.getcwd(), "Report_files")
            array_reports = self.recv_timeout()
            i = 0
            while i < len(array_reports):
                f=open(os.path.join(dir_path, array_reports[i]), 'w')
                f.write(array_reports[i+1])
                f.close()
                i = i + 2
            self.outputReady = "Your report has been printed, go to GUI/Report_files"
            self.consoleOutput()
            self.DisconnectToServer()
        except Exception as e:
            print(e)
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
            self.DisconnectToServer()
        except:
            self.serverConnection = "Server is not working"
            self.consoleOutput()

    def checkConnection(self):
        try:
            self.isItTrained()
            if self.serverConnection != "Server is not working":
                self.serverConnection = "Server is working"
                self.consoleOutput()
        #self.sock.close()
        except:
            pass

    def uCorrection(self):
        try:
            self.ConnectToServer()
            self.sock.sendto(("Correction "+"EndOfCommand").encode('utf-8'), self.server_address)
            time.sleep(0.1)
            self.sock.sendto(self.comboBox.currentText().encode('utf-8').lower(), self.server_address)
            self.fileNameBox.setText("")
            time.sleep(0.1)
            # f = open(str(self.filenames[0][0]), 'r')
            for i in range(0, len(self.filenames[0])):
                self.sendFilesToServer(self.filenames[0][i])
                time.sleep(0.1)
            self.sock.sendall("END OF FILE SENDING".encode())
            data = self.sock.recv(1024)
            if data:
                self.hasCorrected = data.decode()
                self.consoleOutput()
            else:
                self.hasCorrected = "Your correction failed"
                self.consoleOutput()
            self.DisconnectToServer()
        except Exception as e:
            print (e)
            self.hasCorrected = "Your correction failed"
            self.consoleOutput()
            self.DisconnectToServer()

    def consoleOutput(self):
        self.consoleField.setText("Console: \n" + self.serverConnection + "\n" + self.trained + "\n" + self.outputReady + "\n" + self.hasCorrected)

    def verticalFunc(self):
        z = 0
        w = 0
        if self.isFullScreen():
            z = 350
            w = 200
        x = 600 + z
        y = 45
        while y < 450 + w:
            some = QLabel("<b>|</b>", self)
            some.move(x,y)
            y=y+1

    def verticalFSFunc(self):
        x = 950
        y = 45
        while y < 650:
            ome = QLabel("<b>|</b>", self)
            ome.move(x,y)
            y=y+1

    def verticalFuncWin(self):
        x = 1400-self.x
        y = 60
        while y < 1200-self.x:
            some = QLabel("<b>|</b>", self)
            some.move(x,y)
            y=y+1

    def recv_timeout(self,timeout=2):
        #make socket non blocking
        self.sock.setblocking(0)


        #total data partwise in an array
        total_data=[];
        data='';

        #beginning time
        begin=time.time()
        while 1:
            #if you got some data, then break after timeout
            if total_data and time.time()-begin > timeout:
                break

            #if you got no data at all, wait a little longer, twice the timeout
            elif time.time()-begin > timeout*2:
                break

            #recv something
            try:
                data = self.sock.recv(1024)
                if data:
                    total_data.append(data.decode())
                    #change the beginning time for measurement
                    begin=time.time()
                else:
                    #sleep for sometime to indicate a gap
                    time.sleep(0.1)
            except:
                pass

        #join all parts to make final string
        return (total_data)

    def helpFunct(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
                
        msg.setText("This is a help box")
        msg.setInformativeText("This application can be used to train, use, and correct a defect signature classifier.")
        msg.setDetailedText("To check whether the server computer is connected to your computer: Click the “Check Connection” button. The console at the bottom of the application will display “Server is not working” if the server is not connected. If the server is connected, the console will state that the “Server is working.” It will also include information about whether the defect signature classifier has been trained or not. \n\nTo train the defect signature classifier: Click the “Train” button. Wait until you receive the message “Training completed” on the console to continue. This operation will take a while, depending on the architecture of the classifier. Train the classifier whenever new training data has been added to the server computer, a correction was made using the “Correction” button (see below), or the machine has not been trained yet (which can be checked by clicking on the “Check Connection” button). \n\nTo view the defect distribution for a KLA file: Click the “Browse” button to select the KLA file that contains the defects you want to view (note that you may only select one file to view at a time). After selecting the file using “Browse,” click on the “Show plot” button below the address bar. A window will pop up showing the spatial distributions of the defects on the xy-plane. \n\nTo detect and classify any signatures present in the KLA file: Click the “Browse” button to select the KLA file or files that you want to classify. After selecting the file using “Browse,” click on the “Upload” button below the “Browse” button. Wait until you receive the message that “Reports have been generated.” To view the results of the classifications, click the “Print Reports” button. Wait until you receive the message “Your report has been printed, go to GUI/Report_files.” Then, go to <path-to-your-application-code>/Report_files to view your report(s), each of which will be named the same as the timestamp of your input file(s). \nIf you know that the defect signature classifier gave you the wrong classification: Choose the input file that was misclassified by clicking “Browse” and selecting the file. On the right side of the application, under “User Correction,” choose the correct classification from the dropdown at the top. Then, click the “Correction” button. This will make the defect signature classifier less susceptible to misclassifying this signature in the future.")
        
        retval = msg.exec_()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()
        if e.key() == Qt.Key_F:
            if self.isFullScreen():
                self.showNormal1()
            else:
                self.showcaseUI()

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
