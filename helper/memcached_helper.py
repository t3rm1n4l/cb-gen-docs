
import json
import time
from lib.mc_bin_client import MemcachedClient, MemcachedError

class MemcachedHelper(object):
    
    def __init__(self, serverip = "localhost", port = 11211, bucket = "default", password = ""):
        
        self.client = MemcachedClient(serverip, port)
        self.client.sasl_auth_plain(bucket, password)

    def write_one_json(self, key, doc):

        count = 0 
        loaded = False
        while count < 60 and not loaded:
            try:
                self.client.set(key, 0, 0, json.dumps(doc))
                loaded = True
            except MemcachedError as error:
                if error.status == 134:
                    print "Memcached TMP_OOM, Retrying in 5 seconds..."
                    count += 1
                    time.sleep(5)
                elif error.status == 7:
                    print "Not my vbucket error. If on MAC, please specify vbuckets as 64."
                    print "If rebalance is in progress. Please wait for it to finish.\n"
                    break
                else:
                    print error
                    break

    def read_one_json(self, key):

        doc = ""
        try:
            _, _, doc = self.client.get(key)
        except MemcachedError as error:
            print error

        return doc

    def write_batch(self, batch_id, data):
        print "Batch Insert not implemented for Memcached"
