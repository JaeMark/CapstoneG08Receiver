# -*- coding: utf-8 -*-

import threading
import json

DEFAULT_COMMAND = 0
START_COMMAND = 1
SLEEP_COMMAND = 2
WAKE_UP_COMMAND = 3

SAMPLE_NUM = 32
TRANS_DELIM = 16
SMALL_TRANS_DELAY = 250
BIG_TRANS_DELAY = 750

#SLEEP_TIME = 3600000
SLEEP_TIME = 60000
class SerialMsgParser(threading.Thread):
    def __init__(self, dBManager):
        threading.Thread.__init__(self)
        self.dBManager = dBManager
        self.parsedAllSamples = False
        self.sampleParsed  =  0;
    
    def getTrailingData(self, msg):
        lastOpeningIndex = msg.rfind("{")
        lastClosingIndex = msg.rfind("}")
        if lastOpeningIndex > lastClosingIndex:
            trailingDataIndex = msg.rfind("{")
            trailingData = msg[trailingDataIndex:]   
        else:
            trailingData = ""
        return trailingData
    
    def getMsgToParse(self, msg):
        msgToParseEndIndex = msg.rfind("}")
        msgToParse = msg[:msgToParseEndIndex+1]       
        return msgToParse
    
    def setSampleNumToParse(self, sampleNum):
        self.sampleParsed == sampleNum
        return 
    
    def parsedAllSamples(self):
        return self.parsedAllSamples
    
    def getSampleNumParsed(self):
        return self.sampleParsed
    
    def getSleepCommand(self):
        dataToSend = {}
        dataToSend['command'] = SLEEP_COMMAND   
        dataToSend['sleepTime'] = SLEEP_TIME  
        jsonData = json.dumps(dataToSend)
        self.parsedAllSamples = False
        return jsonData
    
    def getStartCommand(self):
        dataToSend = {}
        dataToSend['command'] = START_COMMAND  
        dataToSend['sampleNum'] = SAMPLE_NUM
        dataToSend['delim'] = TRANS_DELIM
        dataToSend['smallDelay'] = SMALL_TRANS_DELAY
        dataToSend['bigDelay'] = BIG_TRANS_DELAY
        #dataToSend['sampleNum'] = self.indexStart
        jsonData = json.dumps(dataToSend)
        return jsonData

    def parseWakeUpCommand(self, msg):
        data = json.loads(msg)
        wakeUpCommand = data['command']
        if(wakeUpCommand == WAKE_UP_COMMAND):
            return True
        return False
                
    def parseReadingData(self, msg, numSamples):
        jsonIndexStart = 0
        jsonIndexEnd = 0
        jsonIndexEndIndex = msg.rfind("}")
        #print("The json end index final is: " + str(jsonIndexEndIndex))
            
        while True:
            if jsonIndexEnd == jsonIndexEndIndex:
                #if(self.sampleParsed == 512):
                #    self.parsedAllSamples == True
                #self.parsedAllSamples = self.dBManager.checkIfSamplingIsDone(numSamples)
                return
            jsonIndexEnd = msg.find("}", jsonIndexStart+1)
            jsonData = msg[jsonIndexStart:jsonIndexEnd+1]
            #print("The json index end is: " +  str(jsonIndexEnd))
            #print("The json data is: " + jsonData)
            if jsonData:
                #print("The json data is: " + jsonData)
                data = json.loads(jsonData)
                #ImID = dataPacket['sampleNum']
                #instant = datetime.datetime.now().isoformat(' ', 'seconds')
                #print("The json data is: " + jsonData)
                volt = data['volt']
                curr = data['curr']
                micros = data['micros']
                #print("The json data is: " + jsonData)
                threading.Thread(target = self.dBManager.storeData(volt, curr, micros)).start()
                #self.dBManager.storeData(jsonData)
                self.sampleParsed += 1
            jsonIndexStart = jsonIndexEnd+1   
        return
