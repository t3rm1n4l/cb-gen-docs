sampledb 
========

- This tool can be used to generate sample dataset for User Profiles and load into Couchbase bucket. 
Optionally, it generates Orders for each User Profile which are loaded as separate JSON documents

python ./gen_user_profiles.py -h

Usage: gen_user_profiles.py [options]

Options:

-h, --help            show this help message and exit

-n NUM_USER_PROFILES, --num_user_profiles=NUM_USER_PROFILES
                        Number of JSON User Profiles to be generated
                        
-s SERVER, --server=SERVER
                        Server Hostname/IP address running Couchbase
                        
-b BUCKET, --bucket=BUCKET
                        Bucket to be loaded with docs
                        
-p PASSWORD, --password=PASSWORD
                        Password for the bucket
                        
-o, --with_orders     Generate Orders for User Profiles(Default is true)
