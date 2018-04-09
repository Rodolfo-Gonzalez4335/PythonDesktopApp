
# fileparsing.py
# class object parses through aKLA fila
# Last updated February 21, 2018
# Rodolfo Gonzalez

# Turn on debug mode.
import cgitb
from wafermappingsignature import wafermappingsignature
import sys
import os
from datetime import datetime
from globalfunctions import deleteFiles

class fileparsing:


    def __init__(self):
        self.lineOfNums = []
        self.defectdensity = "NA"
        self.wafermappings = []
        self.wafer = wafermappingsignature()

    def parse(self):
        print("got in")
        i = 1
        dir_path = os.path.join(os.getcwd(), "input_files")
        for filename in os.listdir(dir_path):
            if filename.endswith(".txt"):
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
                            lotid= lotid.replace("\"","")
                            lotid= lotid.replace(";","")
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
                    # print(self.wafer)
                    self.fileDescriptor.close()
                    self.wafermappings.append(self.wafer)
                    # print(self.wafermappings)

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
        dir_path = os.path.join(os.getcwd(), "Report/")
        temp_dir_path = os.path.join(os.getcwd(), "Report/temp")
        #clearing temp folder
        deleteFiles(temp_dir_path)

        for wafer in self.wafermappings:
            lotId = wafer.lotid.replace(";","")
            f=open(os.path.join(dir_path, lotId+".txt"),'w')
            f.write(str(wafer))
            f.close()
            f1=open(os.path.join(temp_dir_path, lotId+".txt"),'w')
            f1.write(str(wafer))
            f1.close()
        # print (datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])

    def addClassfication(self, classification):
        print (classification)
        for wafer in self.wafermappings:
            print("CLASSIFICATION" + wafer.lotid, classification[1])
            if (wafer.lotid==classification[1]):
                wafer.addClassfication(classification[0])

    def sendReport(self, i):
        if i < len(self.wafermappings):
            return str(self.wafermappings[i])
        else:
            return "DONE"
