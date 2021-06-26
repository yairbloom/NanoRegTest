import pymongo


class ServerChecker:
  def __init__(self):
    MongoClient = pymongo.MongoClient("mongodb://localhost:27017/")
    NanoDB = MongoClient["NanoDB"]

    self.PrintersCollection = NanoDB["printers"]
  def test1(self):

    x = self.PrintersCollection.find_one()


    print(x["Jobs"])


    for x in self.PrintersCollection.find():
      print(x)


if __name__ == "__main__":
  serverChecker = ServerChecker()
  serverChecker.test1()

  
