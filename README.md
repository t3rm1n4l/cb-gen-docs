User Profile Generator 
========

- This tool can be used to generate sample dataset for User Profiles and load into Couchbase bucket or dump to flat files.
Optionally, it generates Orders for each User Profile which are loaded as separate JSON documents. The data generated is deterministic and can be changed using the "seed" argument.

                        python ./gen_user_profiles.py -h



Usage: gen_user_profiles.py [options]

Options:

                        -h, --help             

                        show this help message and exit

                        -N NUM_USER_PROFILES, --num_user_profiles=NUM_USER_PROFILES

                        Number of JSON User Profiles to be generated (Default - 1)
                        
                        -S SERVER, --server=SERVER

                        Server Hostname/IP address running Couchbase (Default - localhost)
                        
                        -b BUCKET, --bucket=BUCKET

                        Bucket to be loaded with docs (Default - default)
                        
                        -p PASSWORD, --password=PASSWORD

                        Password for the bucket (Default - blank)
                        
                        -o, --with_orders     

                        Generate Orders for User Profiles(Default - False)
                        
                        -f, --dump_to_file    
                        Dump User Profiles to file(Default - False)

                        -s SEED, --seed=SEED  
                        Seed value for random generator(Default - 20177)
