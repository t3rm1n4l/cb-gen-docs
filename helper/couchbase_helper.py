
import json

class CouchbaseHelper(object):
    
    def __init__(self, serverip = "localhost", bucket = "default", password = ""):        
        
        try:
            from couchbase import Couchbase
        except ImportError:
            print "Unable to import Couchbase Python Client. Please see http://www.couchbase.com/communities/python/getting-started."
            sys.exit(0)

        self.client = Couchbase.connect(host = serverip, bucket = bucket, username = bucket, password = password)

    def write_one_json(self, key, doc):

        try:
            from couchbase.exceptions import CouchbaseError, TemporaryFailError, NotMyVbucketError
        except ImportError:
            print "Unable to import couchbase.exceptions."
            sys.exit(0)

        count = 0 
        loaded = False
        while count < 60 and not loaded:
            try:
                res = self.client.set(key, doc)
                loaded = True
            except TemporaryFailError:
                    print "Memcached TMP_OOM, Retrying in 5 seconds..."
                    count += 1
                    time.sleep(5)
            except CouchbaseError as error:
                    print error
                    break
            except:
                    print "Unknown Exception Caught!!"
                    break

    def read_one_json(self, key):

        doc = ""
        try:
            doc = self.client.get(key)
        except CouchbaseError as error:
            print error
        return json.dumps(doc.value)

    def write_batch(self, batch_id, data):
        print "Batch Insert not implemented for Couchbase"
