import json

class FileHelper(object):

    def __init__(self):
        pass

    def write_one_json(self, key, doc):

        file_name = "docs/" + key + ".json"
        json_file_handle = open(file_name, "w")
        json_string = json.dumps(doc, sort_keys=True, indent=4, separators=(',', ': '))
        json_file_handle.write(json_string)
        json_file_handle.close()     

    def write_batch(self, batch_id, data):

        file_name = "docs/" + str(batch_id) + ".json"
        json_file_handle = open(file_name, "w")

        for x in xrange(len(data)):
            json_string = json.dumps(data[x])
            json_file_handle.write(json_string)
            json_file_handle.write('\n')

        json_file_handle.close()
