
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
        self.timestamp = "NA"
        self.inspectionstationid = "NA"
        self.lotid = "NA"
        self.samplesize = "NA"
        self.stepid ="NA"
        self.deviceid = "NA"
        self.waferid = "NA"
        self.lineOfNums = []
        self.defectdensity = "NA"
        self.wafermap = wafermappingsignature()

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
                for line in self.fileDescriptor:
                    if 'File Timestamp' in line:
                        timestamp = line[14:-1]
                        self.wafermap.addTimeStamp(timestamp)
                    elif 'InspectionStationID' in line:
                        inspectionstationid = line[20:-1]
                        self.wafermap.addInpectionStationID(inspectionstationid)
                    elif 'LotID' in line:
                        lotid = line[6:-1]
                        self.wafermap.addLotID(lotid)
                    elif 'SampleSize' in line:
                        samplesize = line[11:-1]
                        self.wafermap.addSampleSize(samplesize)
                    elif 'StepID' in line:
                        stepid = line[7:-1]
                        self.wafermap.addStepID(stepid)
                    elif 'DeviceID' in line:
                        deviceid = line[9:-1]
                        self.wafermap.addDeviceID(deviceid)
                    elif 'WaferID' in line:
                        waferid = line[8:-1]
                        self.wafermap.addWaferID(waferid)
                    elif 'DefectList' in line: # Function used since multiple parsing is needed
                        self.parseDefectList()
                    elif 'SummaryList'in line: # This case needs work
                        line = self.fileDescriptor.readline()
                        self.defectdensity = self.getDefectDensity(line)
                        self.wafermap.addDefectDensity(self.defectdensity)
            finally:
                print (self.wafermap)
                self.fileDescriptor.close()

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
            self.wafermap.addToList(self.lineOfNums)
            index = index+1
        # print(self.wafermap)
