import socket
from socket import gethostbyname
import sys
from fileparsing import fileparsing
from wafermappingsignature import wafermappingsignature
import os
import numpy as np
import sys
import matplotlib.pyplot as plt
from keras.models import Sequential,model_from_json
from keras.layers import Conv2D
from keras.layers import AveragePooling2D
from keras.layers import Flatten
from keras.layers import Dense
from keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing import image

class Server(fileparsing):

    def __init__(self):
        # self.training()
        self.host = gethostbyname( '0.0.0.0' )
        #self.host 10.145.31.19
        self.server_address = ("localhost", 10000)
        # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(self.server_address)
        self.sock.listen(1)
        print (sys.stderr, 'starting up on %s port %s' % self.server_address)

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

    def plotFile(self,file_path, index):
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
        plot_name = "classified_images/classified"+str(index)+".png"
        plt.savefig(plot_name)
        plt.close()
        return plot_name

    def isItTrained(self):
        dir_path = os.path.join(os.getcwd())
        for filename in os.listdir(dir_path):
            if filename.endswith(".h5"):
                return True
        return False

    def readCommands(self):
        while True:
            # Wait for a connection
            print ('waiting for a connection')
            connection, client_address = self.sock.accept()
            print (sys.stderr, 'connection from', client_address)
            data = connection.recv(1024)
            data_decoded = data.decode()
            file = fileparsing()
            if "Send Report" in data_decoded:
                #send report function
                directory_path = os.path.join(os.getcwd(), "Report")
                for filename in os.listdir(directory_path):
                    if filename.endswith(".txt"):
                        f = open(os.path.join(directory_path, filename), 'rb')
                        l = f.read(1024)
                        while(l):
                            connection.send(l)
                            l = f.read(1024)
                        f.close()
                connection.close()
            elif "Training mode" in data_decoded:
                self.training()
                connection.sendall("Training completed".encode('utf-8'))
                #connection.close()
            elif "is it trained" in data_decoded:
                if self.isItTrained():
                    connection.sendall("yes".encode('utf-8'))
                else:
                    connection.sendall("no".encode('utf-8'))
            elif not data:
                pass
            else:
                try:
                    i=1
                    # Open file to input_files directory in Server
                    dir_path = os.path.join(os.getcwd(), "input_files")
                    f=open(os.path.join(dir_path, 'file_'+ str(i)+".txt"),'w')
                    i= i+1
                    # Receive the data in small chunks and retransmit it
                    while True:
                        print (sys.stderr, 'received "%s"' % data_decoded)
                        if not data:
                            #case where all files are sent and no more data is being received
                            # print (sys.stderr, 'empty data from client', client_address)
                            f.close()
                            file.parse()
                            break
                        if f.closed and data_decoded!="":
                            # case where multiple files are sent
                            f=open(os.path.join(dir_path, 'file_'+ str(i)+".txt"),'w')
                            i= i+1
                        if "EndOfFile" in data_decoded:
                            first_and_second_file = data_decoded.split("EndOfFile;")
                            f.write(first_and_second_file[0])
                            f.close()
#                            if len(first_and_second_file)==2:
#                                if first_and_second_file[1]!="" or first_and_second_file !=" ":
#                                    f=open(os.path.join(dir_path, 'file_'+ str(i)+".txt"),'w')
#                                    i= i+1
#                                    f.write(first_and_second_file[1])
                        else:
                            f.write(data_decoded)
                        data = connection.recv(1024)
                        data_decoded = data.decode()


                finally:
                    connection.close()
                    classifications = []
                    index = 0
                    for filename in os.listdir(dir_path):
                        if filename.endswith(".txt") :
                            print(dir_path+"/"+filename)
                            image_path = self.plotFile(dir_path+"/" + filename, index)
                            index = index + 1
                            test_image = image.load_img(image_path, target_size = (576, 432))
                            test_image = image.img_to_array(test_image)
                            # print(training_set.class_indices)
                            test_image = np.expand_dims(test_image, axis = 0)
                            json_file = open('model.json','r')
                            loaded_model_json = json_file.read()
                            json_file.close()
                            classifier=model_from_json(loaded_model_json)
                            classifier.load_weights("model.h5")
                            result = classifier.predict(test_image)
                            prediction = ""
                            if result[0][0] == 0:
                                prediction = 'edge_local'
                            elif result[0][0] == 1:
                                prediction = 'electrodes'
                            elif result[0][0] == 2:
                                prediction = 'hotspot'
                            elif result[0][0] == 3:
                                prediction = 'no_pattern'
                            elif result[0][0] == 4:
                                prediction = 'random'
                            elif result[0][0] == 5:
                                prediction = 'slides'
                            elif result[0][0] == 6:
                                prediction = 'spins'
                            elif result[0][0] == 7:
                                prediction = 'sprays'
                            elif result[0][0] == 8:
                                prediction = 'streaks'
                            classifications.append(prediction)
                    i = 0
                    for classification in classifications:
                        file.addClassfication(i, classification)
                        i = i+1
                    file.saveWaferMappings()
server = Server();
server.readCommands();
