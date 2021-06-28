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
    self.PrinterName = f'{time.time()}-Printer'
    self.FileToUpload = os.path.join(os.path.dirname(os.path.realpath(__file__)),'Reference' , 'DC to DC up converter.pcbjc')
    self.PrinterDBItem = None

#########################################################################################################

  def CheckConnection(self):
    res = requests.get(self.BasicUrl)
    return (res.status_code==200)

#########################################################################################################
  def InsertPrinter(self):
    #Sending insert printer request to the server 
    res = requests.post(self.InsertPrinterUrl, 
                        data={'PrinterName':self.PrinterName,'UniqueString':self.PrinterName})
    if res.status_code!=200:
      return False

    #Checking it is exist in the DB
    self.PrinterDBItem = self.PrintersCollection.find_one({'UniqueString':self.PrinterName})
    print(self.PrinterDBItem)

    return self.PrinterDBItem!= None

#########################################################################################################
  def UploadJob(self):
    print(self.FileToUpload)
    with open(self.FileToUpload, 'rb') as f:
      files = {'myFile': (os.path.basename(self.FileToUpload), f, 'application/gzip')}
      data = {'JobName': os.path.basename(self.FileToUpload), 'UniqueString':self.PrinterName}
      res = requests.post(self.NewJobUrl, files=files, data=data)
      if not res or res.status_code!=200:
        return False
      JsonRsp = res.json()
      if not JsonRsp:
        return False
      self.PrinterDBItem = self.PrintersCollection.find_one({'UniqueString':self.PrinterName})
      for JobItem in self.PrinterDBItem['Jobs']:
        if (JobItem['JobPath'] == JsonRsp['JobPath'] and 
            os.path.isfile(JobItem['JobPath']) and 
            os.path.getsize(JobItem['JobPath']) == os.path.getsize(self.FileToUpload)):
          return True
      return False

#########################################################################################################
  def test1(self):

    x = self.PrintersCollection.find_one()


    print(x["Jobs"])


    for x in self.PrintersCollection.find():
      print(x)


if __name__ == "__main__":
  serverChecker = ServerChecker()
  print(serverChecker.CheckConnection())
  print(serverChecker.InsertPrinter())
  print(serverChecker.UploadJob())
  #serverChecker.test1()

  
