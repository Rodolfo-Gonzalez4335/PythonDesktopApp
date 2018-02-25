#Data Strucure for KLA file important all values are stored in this CLASS
#2/21/18
#Rodolfo Gonzalez

class wafermappingsignature:

    def __init__(self):
        self.filetimestamp = "NA"
        self.inpectionstationid = "NA"
        self.lotid = "NA"
        self.samplesize = "NA"
        self.stepid = "NA"
        self.deviceid = "NA"
        self.waferid = "NA"
        self.defectList = []
        self.defectdensity = "NA"

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

    #Debugging method
    def __str__(self):
        toreturn = "TimeStamp: "+self.filetimestamp + "\nStation ID: " + self.inpectionstationid+"\nLotId: " + self.lotid+ "\nSampleSize: "+ self.samplesize + "\nStepID: "+ self.stepid + "\nDeviceID: " + self.deviceid + "\nWaferId"    + self.waferid + "\nDefectList: \n"
        i=0;

        for x in range(len(self.defectList)):
            toreturn = toreturn + str(self.defectList[x])
            toreturn=toreturn+"\n"
            i = i+1;
        toreturn = toreturn +"\n"+ str(self.defectdensity)
        return toreturn
