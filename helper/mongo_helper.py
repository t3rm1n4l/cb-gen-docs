
class MongoHelper(object):
    
    def __init__(self, serverip = "localhost", port = 27017, database = "sampledb", collection = "user_profile"):

        try:
            from pymongo import MongoClient
        except ImportError:
            print "Unable to import MongoClient from pymongo. Please see http://api.mongodb.org/python/current/installation.html"
            sys.exit(0)

        self.client = MongoClient(serverip, port)
        self.db = self.client[database]
        self.collection = self.db[collection]

    def write_one_json(self, key, doc):

        doc["_id"] = key
        self.collection.insert(doc)


    def read_one_json(self, key):

        return self.collection.find_one({"_id": key})

