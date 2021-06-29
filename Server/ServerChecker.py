import pymongo
import requests
import time
import os.path


class ServerChecker:
  def __init__(self):
    MongoClient = pymongo.MongoClient("mongodb://localhost:27017/")
    NanoDB = MongoClient["NanoDB"]

    self.PrintersCollection = NanoDB["printers"]
    self.BasicUrl = 'http://localhost:3000/' 
    self.InsertPrinterUrl = self.BasicUrl + 'printers/AddPrinter'
    self.NewJobUrl = self.BasicUrl + 'printers/NewJob'
    self.GetJobInfoUrl = self.BasicUrl + 'printers/GetJobInfo'
    self.UpdateJobMetadataUrl = self.BasicUrl + 'printers/UpdateJobMetadata'
    self.GetNextJobDetailsUrl = self.BasicUrl + 'printers/GetNextJobDetails'
    self.GetJobUrl = self.BasicUrl + 'printers/GetJob'
    self.NotifyJobActiveUrl = self.BasicUrl + 'printers/NotifyJobActive'

    self.PrinterName = f'{time.time()}-Printer'
    self.FileToUpload = os.path.join(os.path.dirname(os.path.realpath(__file__)),'Reference' , 'DC to DC up converter.pcbjc')

#########################################################################################################

  def CheckConnection(self):
    Ret = True
    ErrStr = ''
    try:
      res = requests.get(self.BasicUrl)
      Ret = res and res.status_code==200
    except Exception as e:
      Ret = False
      ErrStr = str(e)
         
    print(f'CheckConnection {Ret} {ErrStr}')
    return Ret


#########################################################################################################
  def InsertPrinter(self):
    #Sending insert printer request to the server 
    Ret = True
    ErrStr = ''
    try:
      res = requests.post(self.InsertPrinterUrl, 
                          data={'PrinterName':self.PrinterName,'UniqueString':self.PrinterName})
      Ret = res and (res.status_code==200)

      #Checking it is exist in the DB
      if Ret:
        Ret = self.PrintersCollection.find_one({'UniqueString':self.PrinterName}) != None
    except Exception as e:
      Ret = False
      ErrStr = str(e)
         
    print(f'InsertPrinter {Ret} {ErrStr}')
    return Ret


#########################################################################################################
  def GetNextJobDetails(self , ExpectedStatusCode):
    Ret = True
    ErrStr = ''
    ResJaon = None
    try:
      res = requests.get(self.GetNextJobDetailsUrl , params={'PrinterIdentifier':self.PrinterName})
      Ret = res and res.status_code == ExpectedStatusCode
      if Ret and res.status_code == 200:
        ResJaon = res.json()
        
    except Exception as e:
      Ret = False
      ErrStr = str(e)
         
    print(f'GetNextJobDetails {Ret} {ErrStr}')
    return Ret , ResJaon

#########################################################################################################
  def UploadJob(self):
    Ret = True
    ErrStr = ''
    try:
      with open(self.FileToUpload, 'rb') as f:
        files = {'myFile': (os.path.basename(self.FileToUpload), f, 'application/gzip')}
        data = {'JobName': os.path.basename(self.FileToUpload), 'UniqueString':self.PrinterName}
        #send NewJob request to the server 
        res = requests.post(self.NewJobUrl, files=files, data=data)
        Ret = res and res.status_code==200
        if Ret:
          JsonRsp = res.json()
        Ret = Ret and JsonRsp
        if Ret:
          Ret = False
          #Check that new job updated on the DB
          PrinterDBItem = self.PrintersCollection.find_one({'UniqueString':self.PrinterName})
          for JobItem in PrinterDBItem['Jobs']:
            if (JobItem['JobPath'] == JsonRsp['JobPath'] and 
                os.path.isfile(JobItem['JobPath']) and 
                os.path.getsize(JobItem['JobPath']) == os.path.getsize(self.FileToUpload)):
             Ret = True
    except Exception as e:
      Ret = False
      ErrStr = str(e)
         
    print(f'UploadJob {Ret} {ErrStr}')
    return Ret

#########################################################################################################
 
if __name__ == "__main__":
  serverChecker = ServerChecker()
  RetVal = True
  if RetVal:
    RetVal = serverChecker.CheckConnection()
  if RetVal:
    RetVal = serverChecker.InsertPrinter()
  if RetVal:
    RetVal,ResJaon = serverChecker.GetNextJobDetails(204) # Check That Jobs list is empty
  if RetVal:
    RetVal = serverChecker.UploadJob()
  if RetVal:
    RetVal,ResJaon = serverChecker.GetNextJobDetails(200) # Check That Jobs list is not empty
  if RetVal :
    print('Pass: All Tests')
  #serverChecker.test1()

  
