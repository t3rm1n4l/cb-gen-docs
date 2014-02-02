#!/usr/bin/env python
# -*- python -*-


##TODO 
# add support for batch loading and see the perf difference
# add support for deletion as well

import os
import json
import random
from optparse import OptionParser

from helper.memcached_helper import MemcachedHelper
from helper.mongo_helper import MongoHelper
from helper.couchbase_helper import CouchbaseHelper
from helper.file_helper import FileHelper

from generator.user_profile_gen import UserProfileGenerator
from generator.order_gen import OrderGenerator

def main():

    parser = OptionParser()
    parser.add_option("-N", "--num_user_profiles", dest="num_user_profiles", type = "int", default = 1,
                  help="Number of JSON User Profiles to be generated (Default - 1)")
    parser.add_option("-S", "--server", dest="server", default = "localhost",
                  help="Server Hostname/IP address running Couchbase (Default - localhost)")
    parser.add_option("-b", "--bucket", dest="bucket", default = "default",
                  help="Bucket to be loaded with docs (Default - default)")
    parser.add_option("-p", "--password", dest="password", default="",
                  help="Password for the bucket (Default - blank)")
    parser.add_option("-o", "--with_orders", action="store_true", dest="with_orders", default=False,
                  help="Generate separate JSON Documents for each order in User Profile(Default - False)")
    parser.add_option("-s", "--seed", dest="seed", type = "int", default = 20177,
                  help="Seed value for random generator(Default - 20177)")
    parser.add_option("-c", "--cb_client", dest="cb_client", action="store_true", default = False,
                  help="Use Couchbase Python Client(Default - False)")
    parser.add_option("-m", "--dump_to_mongo", action="store_true", dest="dump_to_mongo", default=False,
                  help="Dump User Profiles to Mongo(Default - False)")
    parser.add_option("-f", "--dump_to_file", action="store_true", dest="dump_to_file", default=False,
                  help="Dump User Profiles to file(Default - False)")
    parser.add_option("-B", "--batch_size", dest="batch_size", type = "int", default = 1,
                  help="Batch Size for Data Load")
    parser.add_option("-M", "--mutation_mode", dest="mutation_mode", type = "int", default = 0,
                  help="Mutate data after loading. 0(Off) by default. 1 - 80/20(R/W). 2 - 50/50(R/W).")
    parser.add_option("-d", "--dev", dest="isdev", action = "store_true", default = False,
                  help="Use development ports")


    (options, args) = parser.parse_args()
    
    profile_gen = UserProfileGenerator(options.mutation_mode)
    
    random.seed(options.seed)

    json_loader = pick_json_loader(options)
    
    generate_and_load_user_profiles(profile_gen, json_loader, options) 
    
    if options.mutation_mode > 0:
        mutate_user_profiles(profile_gen, json_loader, options)   


def generate_and_load_user_profiles(profile_gen, json_loader, options):

    print "Generating {0} User Profiles...".format(options.num_user_profiles)

    user_profiles = []
    orders = []
    order_gen = OrderGenerator()

    for x in xrange(options.num_user_profiles):
        user_profiles.append(profile_gen.create_single_user_profile())

        if options.with_orders:
            curr_profile = len(user_profiles) - 1
            orders.append(order_gen.generate_orders_from_history(user_profiles[curr_profile]["shipped_order_history"]))

        if options.batch_size == 1:
            json_loader.write_one_json(user_profiles[0]["profile_details"]["user_id"], user_profiles[0])
            user_profiles[:] = []
        elif (x + 1) % options.batch_size == 0:
            batch_id = (x + 1)/options.batch_size
            json_loader.write_batch(batch_id, user_profiles)
            user_profiles[:] = []

        if options.with_orders:
            if options.batch_size == 1:
                for n in xrange(len(orders[0])):
                    json_loader.write_one_json(orders[0][n]["order_details"]["order_id"], orders[0][n])
                orders[:] = []
            elif (x + 1) % options.batch_size == 0:
                batch_id = (x + 1)/options.batch_size
                for n in xrange(len(orders)):
                    json_loader.write_batch(batch_id, orders[n])
                orders[:] = []

    print "Done!!"


def pick_json_loader(options):
    
    json_loader = 0
    if options.dump_to_file:
        json_loader = FileHelper()
        print "Storing Data in Flat Files in docs/ folder"

    elif options.dump_to_mongo:
        print "Loading Data to MongoDB using python client"
        json_loader = MongoHelper(options.server)

    elif options.cb_client:
        print "Loading Data to Couchbase using python client"
        json_loader = CouchbaseHelper(options.server, options.bucket, options.password)

    else:
        print "Loading Data to Couchbase using memcached client"
        if options.isdev:
            port = 11999
        else:
            port = 11211

        json_loader = MemcachedHelper(options.server, port, options.bucket, options.password)
            
    return json_loader

def mutate_user_profiles(profile_gen, json_loader, options):

    print "Starting Mutation!! Kill me when done!!"

    mutation_list = profile_gen.get_mutation_list()

    while True:
        
        if options.num_user_profiles < 10:
            print "Too few docs to mutate. Need > 10"
            break
        elif options.num_user_profiles < 10000:
            mutation_count_max = options.num_user_profiles - 10
        else:
            mutation_count_max = 9990
        
        mutation_pick = random.randint(0, mutation_count_max)

        ##80/20(R/W)
        if options.mutation_mode == 1:

            for i in xrange(8):
                doc = json_loader.read_one_json(mutation_list[mutation_pick + i])
                if (i==0) or (i==1):
                    json_loader.write_one_json(mutation_list[mutation_pick + i], json.loads(doc))

        ##50/50(R/W)
        elif options.mutation_mode == 2:

            for i in xrange(5):
                doc = json_loader.read_one_json(mutation_list[mutation_pick + i])
                json_loader.write_one_json(mutation_list[mutation_pick + i], json.loads(doc))

        else:
            print "Invalid Mutation Mode!!"


if __name__ == '__main__':
    main()
    os._exit(0)
