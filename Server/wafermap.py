#Data Strucure for KLA file important all values are stored in this CLASS
#2/21/18
#Rodolfo Gonzalez

class wafermap:

    def __init__(self):
        self.filetimestamp = "NA"
        self.inpectionstationid = "NA"
        self.lotid = "NA"
        self.samplesize = "NA"
        self.setupID = "NA"
        self.stepid = "NA"
        self.deviceid = "NA"
        self.waferid = "NA"
        self.defectList = []
        self.defectdensity = "NA"
        self.classification = "NA"

    def addTimeStamp(self,timestamp):
        self.filetimestamp = timestamp

    def addInpectionStationID(self,inspectionstationid):
        self.inpectionstationid = inspectionstationid

    def addLotID(self, lotid):
        self.lotid = lotid

    def addSampleSize(self,samplesize):
        self.samplesize = samplesize

    def addStepID(self, stepid):
        self.stepid = stepid

    def addDeviceID(self,deviceid):
        self.deviceid = deviceid

    def addWaferID(self, waferid):
        self.waferid = waferid

    def addDefectDensity(self, defectdensity):
        self.defectdensity = defectdensity

    def addDefectDensity(self, item):
        self.defectdensity = item;

    def addToList(self,item):
        self.defectList.append(item)

    def addtoDefectList(self, defectlist):
        self.defectList += defectlist

    def addclassiFication(self, classification):
        self.classification = classification

    def addSetupID(self,setupid):
        self.setupID = setupid
    #Debugging method
    def __str__(self):
        toreturn = "WaferId"+ self.waferid+"\nClassification: "+self.classification+"\n========================================"+"\nLotId: " + self.lotid+ "\nStepID: "+ self.stepid+"\nSetupID"+self.setupID+ "\nDeviceID: " + self.deviceid +"\nStation ID: " + self.inpectionstationid+ "\nSampleSize: "+ self.samplesize+"\nTimeStamp: "+self.filetimestamp+"\nEOF"
        # toreturn = self.timestamp+"\t\t\t"+self.inpectionstationid+"\t\t\t"+self.lotid+"\t\t\t"+self.samplesize+"\t\t\t"SampleSize\t\t\tStepID\t\t\tDeviceID\t\t\tWaferID
        # i=0;
        #
        # for x in range(len(self.defectList)):
        #     toreturn = toreturn + str(self.defectList[x])
        #     toreturn=toreturn+"\n"
        #     i = i+1;
        # toreturn = toreturn +"\n"+ str(self.defectdensity)
        return toreturn
