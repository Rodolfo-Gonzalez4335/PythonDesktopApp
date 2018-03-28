
# fileparsing.py
# class object parses through aKLA fila
# Last updated February 21, 2018
# Rodolfo Gonzalez

# Turn on debug mode.
import cgitb
from wafermappingsignature import wafermappingsignature
import sys
import os

class fileparsing:


    def __init__(self):
        self.lineOfNums = []
        self.defectdensity = "NA"
        self.wafermappings = []
        self.wafer = wafermappingsignature()

    def parse(self):
        i = 1
        dir_path = os.path.join(os.getcwd(), "input_files")
        for filename in os.listdir(dir_path):
            if filename == ".DS_Store":
                break
            try:
                self.fileDescriptor = open(os.path.join(dir_path, filename), "r")
            except OSError:
                print ("File could not be opened")
            try:
                self.wafer = wafermappingsignature()
                for line in self.fileDescriptor:
                    if 'File Timestamp' in line:
                        timestamp = line[14:-1]
                        self.wafer.addTimeStamp(timestamp)
                    elif 'InspectionStationID' in line:
                        inspectionstationid = line[20:-1]
                        self.wafer.addInpectionStationID(inspectionstationid)
                    elif 'LotID' in line:
                        lotid = line[6:-1]
                        self.wafer.addLotID(lotid)
                    elif 'SampleSize' in line:
                        samplesize = line[11:-1]
                        self.wafer.addSampleSize(samplesize)
                    elif 'SetupID' in line:
                        setupID = line[8:-1]
                        self.wafer.addSetupID(setupID)
                    elif 'StepID' in line:
                        stepid = line[7:-1]
                        self.wafer.addStepID(stepid)
                    elif 'DeviceID' in line:
                        deviceid = line[9:-1]
                        self.wafer.addDeviceID(deviceid)
                    elif 'WaferID' in line:
                        waferid = line[8:-1]
                        self.wafer.addWaferID(waferid)
                    elif 'DefectList' in line: # Function used since multiple parsing is needed
                        self.parseDefectList()
                    elif 'SummaryList'in line: # This case needs work
                        line = self.fileDescriptor.readline()
                        self.defectdensity = self.getDefectDensity(line)
                        self.wafer.addDefectDensity(self.defectdensity)
            finally:

                self.fileDescriptor.close()
                self.wafermappings.append(self.wafer)

    def getDefectDensity(self, line):
        list = line.strip(' ').split(' ')
        return float(list[2])

    def parseDefectList(self):
        index=0;
        for line in self.fileDescriptor:
            if 'SummarySpec' in line:
                # self.fileDescriptor.seek(pos)
                break
            self.lineOfNums = []
            linelist = line.strip(' ').split(' ')
            i=0;
            for num in linelist:
                #removes first and last elements
                if i==0 or i>9:
                    i+=1
                    continue
                #value conversion
                elif i==3:
                    i+=1
                    if float(num)==0.0:
                        num=1;
                    self.lineOfNums[0] = self.lineOfNums[0]*float(num);
                    continue
                elif i ==4:
                    i+=1
                    if float(num)==0.0:
                        num=1;
                    self.lineOfNums[1] = self.lineOfNums[1]*float(num);
                    continue
                try:
                    self.lineOfNums.append(float(num))
                except ValueError:
                    if num!="":
                        num = num[:-2]
                        self.lineOfNums.append(float(num))
                    pass
                i+=1
                #Line of code used for end of defect list fileparsing
            self.wafer.addToList(self.lineOfNums)
            index = index+1
        # print(self.wafermap)
    def saveWaferMappings(self):
        dir_path = os.path.join(os.getcwd(), "Report")
        i=0
        for wafer in self.wafermappings:
            i+=1
            f=open(os.path.join(dir_path, 'file_'+ str(i)+".txt"),'w')
            # f.write("Timestamp\t\t\tInpectionId\t\t\tLotID\t\t\tSampleSize\t\t\tStepID\t\t\tDeviceID\t\t\tWaferID\n")
            f.write(str(wafer))

    def addClassfication(self,index,classification):
        if len(self.wafermappings)<index:
            print("INDEX IS OUT OF BOUNDS!")
        else:
            self.wafermappings[index].addClassfication(classification)
