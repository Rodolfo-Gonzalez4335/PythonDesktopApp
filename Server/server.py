import socket
from socket import gethostbyname
import sys
from fileparsing import fileparsing
from wafermappingsignature import wafermappingsignature
import os
import numpy as np
import time
import sys
import matplotlib.pyplot as plt
from keras.models import Sequential,model_from_json
from keras.layers import Conv2D
from keras.layers import AveragePooling2D
from keras.layers import Flatten
from keras.layers import Dense
from keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing import image
from datetime import datetime
from globalfunctions import deleteFiles,cleanString,moveFilesToFilePath

class Server(fileparsing):

    def __init__(self):
        self.host = gethostbyname( '0.0.0.0' )
        # self.server_address = ("localhost", 10000)
        self.server_address = (self.host, 10000)
        # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(self.server_address)
        self.sock.listen(1)
        # print (sys.stderr, 'starting up on %s port %s' % self.server_address)

    def training(self):
        print("Training Neural Net")
        classifier = Sequential()
        classifier.add(Conv2D(32, (3, 3), input_shape = (576, 432, 3), activation = 'relu'))
        classifier.add(AveragePooling2D(pool_size = (2, 2)))
        classifier.add(Flatten())
        classifier.add(Dense(units = 128, activation = 'relu'))  # Experiment with different powers of 2 for units
        classifier.add(Dense(units = 9, activation = 'sigmoid'))
        classifier.compile(optimizer = 'adam', loss = 'categorical_crossentropy', metrics = ['categorical_accuracy'])
        train_datagen = ImageDataGenerator(rescale = 1./255,
        shear_range = 0.2,
        zoom_range = 0.2,
        horizontal_flip = True)
        test_datagen = ImageDataGenerator(rescale = 1./255)
        training_set = train_datagen.flow_from_directory('training_set',
        target_size = (576, 432),
        batch_size = 32,
        class_mode = 'categorical')
        test_set = test_datagen.flow_from_directory('test_set',
        target_size = (576, 432),
        batch_size = 32,
        class_mode = 'categorical')
        classifier.fit_generator(training_set,
        steps_per_epoch = 1,
        epochs = 1,
        validation_data = test_set,
        validation_steps = 1)
        model_json = classifier.to_json();
        with open("model.json", "w") as json_file:
            json_file.write(model_json)
        classifier.save_weights("model.h5")
        print("Finished Training")

    def column(self,matrix, i):
        return [row[i] for row in matrix]

    def plotFile(self,file_path,file_name):
        try:
            file = open(file_path,"r")
            array_of_nums = []
            # name = []
            for line in file:
                if 'FileTimestamp' in line:
                    timestamp = line[14:-1]
                    timestamp = cleanString(timestamp)
                if 'DefectList' in line:
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
            file_name= file_name.replace(".txt","")
            # my_path = os.path.abspath(__file__)
            plot_name = os.path.join(os.getcwd(), "classified_images/",timestamp)
            plt.savefig('{}.png'.format(plot_name))
            plt.close()
            return plot_name
        except Exception as e:
            print (e)

    def sendReport(self):
        directory_path = os.path.join(os.getcwd(), "Report/")
        # print(directory_path)
        for filename in os.listdir(directory_path):
            # print(filename)
            if filename.endswith(".txt"):
                self.connection.send(filename.encode('utf-8'))
                f = open(os.path.join(directory_path, filename), 'rb')
                l = f.read(1024)
                while(l):
                    self.connection.send(l)
                    l = f.read(1024)
                time.sleep(0.1);
                f.close()

    def isItTrained(self):
        dir_path = os.path.join(os.getcwd())
        for filename in os.listdir(dir_path):
            if filename.endswith(".h5"):
                return True
        return False

    def correction(self, data_decoded):
        try:
            dir_path = os.path.join(os.getcwd(), "input_files")
            deleteFiles(dir_path)

            data = self.connection.recv(1024)
            data_decoded = data.decode()
            self.receiveAndWriteFiles(data,data_decoded)
            return True

        except Exception as e:
            print(e)
            return False

    def receiveAndWriteFiles(self, data,data_decoded):
        try:
            dir_path = os.path.join(os.getcwd(), "input_files")
            deleteFiles(dir_path)

            i=1
            dir_path = os.path.join(os.getcwd(), "input_files")
            f=open(os.path.join(dir_path, 'file_'+ str(i)+".txt"),'w')
            i= i+1
            while True:
                # print (sys.stderr, 'received "%s"' % data_decoded)
                if not data:
                    #case where all files are sent and no more data is being received
                    f.close()
                    self.wafermappings.parse()
                    break
                if "END OF FILE SENDING" in data_decoded:
                    break
                # case where multiple files are sent in one data package
                if f.closed and data_decoded!="":
                    f=open(os.path.join(dir_path, 'file_'+ str(i)+".txt"),'w')
                    i= i+1

                if "EndOfFile" in data_decoded:
                    first_and_second_file = []
                    indexEOF = data_decoded.find("EndOfFile")
                    first_and_second_file.append(data_decoded[0:indexEOF])
                    first_and_second_file.append(data_decoded[indexEOF+12:-1])
                    f.write(first_and_second_file[0])
                    f.close()
                    if  "FileVersion" in first_and_second_file[1]:
                        f=open(os.path.join(dir_path, 'file_'+ str(i)+".txt"),'w')
                        i= i+1
                        f.write(first_and_second_file[1])

                else:
                    f.write(data_decoded)
                data = self.connection.recv(1024)
                data_decoded = data.decode()
            return True
        except Exception as e:
            print (e)
            return False

    def readCommands(self):
        while True:
            # Wait for a connection
            # print ('waiting for a connection')
            self.connection, client_address = self.sock.accept()
            # print (sys.stderr, 'connection from', client_address)
            data = self.connection.recv(1024)
            data_decoded = data.decode()
            self.wafermappings = fileparsing()
            if "Send Report" in data_decoded:
                self.sendReport()
                self.connection.close()
            elif "Training mode" in data_decoded:
                self.training()
                self.connection.sendall("Training completed".encode('utf-8'))
            elif "is it trained" in data_decoded:
                if self.isItTrained():
                    self.connection.sendall("yes".encode('utf-8'))
                else:
                    self.connection.sendall("no".encode('utf-8'))
            elif not data:
                pass
            elif "Correction" in data_decoded:
                data = self.connection.recv(1024)
                data_decoded = data.decode()
                # print(data_decoded)
                if (self.correction(data_decoded)):
                    self.connection.sendall("Succesfully made correction".encode("utf-8"))
                else:
                    self.connection.sendall("Failed to send correction".encode("utf-8"))
                self.connection.close()
                self.createImagesFromTxt()
                imagesPath =os.path.join(os.getcwd(), "classified_images/")
                movePath = os.path.join(os.getcwd(), "training_set/",data_decoded)
                moveFilesToFilePath(imagesPath,movePath)
                # print("Connection Closed")
            else:
                self.receiveAndWriteFiles(data,data_decoded)
                self.connection.close()
                classifications = []
                self.createImagesFromTxt()
                self.classifyDefects()


    def createImagesFromTxt(self):
        # print (datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
        try:
            dir_path = os.path.join(os.getcwd(), "input_files/")
            # print("Creating images")
            for filename in os.listdir(dir_path):
                # print("Plotting " + filename)
                if filename.endswith(".txt") :
                    image_path = self.plotFile(dir_path+ filename,filename)
            # print (datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
        except Exception as e:
            print (e)

    def classifyDefects(self):
        # print (datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
        try:
            dir_path = os.path.join(os.getcwd(),"classified_images/")
            classifications=[]

            for filename in os.listdir(dir_path):
                if filename.endswith(".png") :
                    test_image = image.load_img("classified_images/"+filename, target_size = (576, 432))
                    test_image = image.img_to_array(test_image)
                    # print(training_set.class_indices)
                    test_image = np.expand_dims(test_image, axis = 0)
                    json_file = open('model.json','r')
                    loaded_model_json = json_file.read()
                    json_file.close()
                    classifier=model_from_json(loaded_model_json)
                    classifier.load_weights("model.h5")
                    result = classifier.predict(test_image)
                    timestamp = filename.replace(".png","")
                    classifications.append([self.prediction(result),timestamp])

            #adding the classification to the wafer mappings
            for classification in classifications:
                self.wafermappings.addclassiFication(classification)

            #wafermappings is the data structure that has all the signatures
            self.wafermappings.saveWaferMappings()
            # print (datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
        except Exception as e:
            print(e)
    def prediction(self,result):
        if result[0][0] == 0:
            return 'edge_local'
        elif result[0][0] == 1:
            return 'electrodes'
        elif result[0][0] == 2:
            return 'hotspot'
        elif result[0][0] == 3:
            return 'no_pattern'
        elif result[0][0] == 4:
            return 'random'
        elif result[0][0] == 5:
            return 'slides'
        elif result[0][0] == 6:
            return 'spins'
        elif result[0][0] == 7:
            return 'sprays'
        elif result[0][0] == 8:
            return 'streaks'
server = Server();
#server.createImagesFromTxt()
server.readCommands();
