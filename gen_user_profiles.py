import os
import json
import random
from datetime import datetime, timedelta
from optparse import OptionParser

from lib.mc_bin_client import MemcachedClient, MemcachedError

class UserProfile(object):

    def __init__(self):
        self.user_id = None
        self.password = None
        self.user_creation_time = None
        self.last_login_time = None

        self.user_creation_time_str = None
        self.last_login_time_str = None

        self.ui_theme = None
        self.ui_language = None
        self.promotion_email = None
        self.promotion_category = []

        self.first_name = None
        self.last_name = None
        self.display_name = None
        self.age = None
        self.email = None
        self.state = None

        self.loyalty_score = None
        self.membership_type = None
        self.reward_points = None
        self.redeemed_points = None
        self.friends_referred = []

        self.order_history = []

        self.most_searched = []

class Order(object):


    def __init__(self):

        self.order_id = None
        self.order_datetime = None

        self.product_id = None
        self.list_price = None
        self.pct_discount = None
        self.sale_price = None
        self.currency = None

        self.shipping_type = None
        self.shipping_charges = None
        self.shipping_status = None

        self.total_charges = None
        self.payment_mode = None

class OrderGenerator(object):
    
    def __init__(self):
        self.orders = []

    def generate_orders_from_history(self, order_history_list):

        for i in xrange(len(order_history_list)):
            order = self.generate_single_order(order_history_list[i])
            self.orders.append(self.package_order(order))

        return self.orders

    def package_order(self, order):
     
        order_map = {}
        order_map["doc_type"] = "order"
        order_map["product_details"] = {}
        order_map["shipping_details"] = {}
        order_map["payment_details"] = {}
        order_map["order_details"] = {}

        order_map["order_details"]["order_id"] = order.order_id
        order_map["order_details"]["order_datetime"] = order.order_datetime

        order_map["product_details"]["product_id"] = order.product_id
        order_map["product_details"]["list_price"] = order.list_price
        order_map["product_details"]["pct_discount"] = order.pct_discount
        order_map["product_details"]["sale_price"] = order.sale_price
        order_map["product_details"]["currency"] = order.currency

        order_map["shipping_details"]["shipping_type"] = order.shipping_type
        order_map["shipping_details"]["shipping_charges"] = order.shipping_charges
        order_map["shipping_details"]["shipping_status"] = order.shipping_status

        order_map["payment_details"]["total_charges"] = order.total_charges
        order_map["payment_details"]["payment_mode"] = order.payment_mode

        return order_map

    def generate_single_order(self, order_history):

        self.order = Order()
        
        self.order.order_id = order_history["order_id"]
        self.order.order_datetime = order_history["order_datetime"]

        self.gen_product_details()
        self.gen_shipping_details()
        self.gen_payment_details()

        return self.order

    def gen_product_details(self):
        self.gen_product_id()
        self.gen_pricing_details()

    def gen_shipping_details(self):

        shipping_type = ["Express", "Overnight", "Regular", "Priority"]
        shipping_charges = [ 5, 10, 2, 15]
        choice = random.randint(0, len(shipping_type) - 1)
        self.order.shipping_type = shipping_type[choice]
        self.order.shipping_charges = shipping_charges[choice]

        self.order.shipping_status = "Delivered"

    def gen_payment_details(self):
        self.gen_total_charges()
        self.gen_payment_mode()

    def gen_product_id(self):
        self.order.product_id = "P" + str(random.randint(100000, 1000000)) + str(random.randint(2000, 7000))

    def gen_pricing_details(self):
        self.order.list_price = random.randint(20, 1000)
        pct_discount = [5, 10, 15, 20, 25]
        self.order.pct_discount = random.choice(pct_discount)
        self.order.sale_price = self.order.list_price - (self.order.list_price * self.order.pct_discount / 100)
        currency = ["USD", "EUR", "GBP"]
        self.order.currency = random.choice(currency)

    def gen_total_charges(self):
        self.order.total_charges = self.order.sale_price + self.order.shipping_charges

    def gen_payment_mode(self):
        payment_mode = ["Credit Card", "Cash On Delivery", "Debit Card", "Reward Points", "NetBanking"]
        self.order.payment_mode = random.choice(payment_mode)


class UserProfileGenerator(object):

    def __init__(self):

        self.fn_master_list = []
        self.ln_master_list = []
        self.state_master_list = []
        self.user_id_master = []

        self.read_master_data()		

    def read_master_data(self):
        FIRST_NAME_FILE = "data/firstname.dat"
        LAST_NAME_FILE = "data/lastname.dat"
        STATE_NAME_FILE = "data/states.dat"

        ##read the master files into lists
        if not os.path.exists(FIRST_NAME_FILE):
            print "FIRST NAME DATA FILE IS MISSING. EXITTING!!!"
            exit(-1)

        fn_file_handle = open(FIRST_NAME_FILE)
        for line in fn_file_handle:
            self.fn_master_list = line.split(',')

        fn_file_handle.close()

        if not os.path.exists(LAST_NAME_FILE):
            print "LAST NAME DATA FILE IS MISSING. EXITTING!!!"
            exit(-1)

        ln_file_handle = open(LAST_NAME_FILE)
        for line in ln_file_handle:
            self.ln_master_list = line.split(',')

        ln_file_handle.close()

        if not os.path.exists(STATE_NAME_FILE):
            print "STATE NAME DATA FILE IS MISSING. EXITTING!!!"
            exit(-1)

        state_file_handle = open(STATE_NAME_FILE)
        for line in state_file_handle:
            self.state_master_list = line.split(',')

        state_file_handle.close()

    def package_user_profile(self):
        user_profile_map = {}
        user_profile_map["doc_type"] = self.user_profile.doc_type
        user_profile_map["profile_details"] = {}
        user_profile_map["personal_details"] = {}
        user_profile_map["profile_details"]["prefs"] = {}
        user_profile_map["profile_details"]["loyalty"] = {}

        user_profile_map["profile_details"]["user_id"] = self.user_profile.user_id
        user_profile_map["profile_details"]["password"] = self.user_profile.password
        user_profile_map["profile_details"]["last_login_time"] = self.user_profile.last_login_time_str
        user_profile_map["profile_details"]["user_creation_time"] = self.user_profile.user_creation_time_str

        user_profile_map["personal_details"]["first_name"] = self.user_profile.first_name
        user_profile_map["personal_details"]["last_name"] = self.user_profile.last_name
        user_profile_map["personal_details"]["display_name"] = self.user_profile.display_name
        user_profile_map["personal_details"]["age"] = self.user_profile.age
        user_profile_map["personal_details"]["email"] = self.user_profile.email
        user_profile_map["personal_details"]["state"] = self.user_profile.state

        user_profile_map["profile_details"]["prefs"]["ui_theme"] = self.user_profile.ui_theme
        user_profile_map["profile_details"]["prefs"]["ui_language"] = self.user_profile.ui_language
        user_profile_map["profile_details"]["prefs"]["promotion_email"] = self.user_profile.promotion_email
		
        if self.user_profile.promotion_email:
           user_profile_map["profile_details"]["prefs"]["promotion_category"] = self.user_profile.promotion_category

        user_profile_map["profile_details"]["loyalty"]["loyalty_score"] = self.user_profile.loyalty_score
        user_profile_map["profile_details"]["loyalty"]["membership_type"] = self.user_profile.membership_type
        user_profile_map["profile_details"]["loyalty"]["reward_points"] = self.user_profile.reward_points
        user_profile_map["profile_details"]["loyalty"]["redeemed_points"] = self.user_profile.redeemed_points
        user_profile_map["profile_details"]["loyalty"]["friends_referred"] = self.user_profile.friends_referred

        user_profile_map["order_history"] = self.user_profile.order_history
 
        if len(self.user_profile.most_searched):
            user_profile_map["most_searched"] =  self.user_profile.most_searched
 
        return user_profile_map

    def create_single_user_profile(self):

        self.user_profile = UserProfile()
       
        self.gen_document_type()
        self.gen_personal_details()
        self.gen_profile_details()
        self.gen_order_history()
        self.gen_most_searched()
        return self.package_user_profile()

    def gen_personal_details(self):

        self.gen_first_name()
        self.gen_last_name()
        self.gen_display_name()
        self.gen_age()
        self.gen_email()
        self.gen_state()

    def gen_profile_details(self):

        self.gen_user_id()
        self.gen_password()
        self.gen_usercreationtime()
        self.gen_lastlogintime()
 
        self.gen_user_prefs()
        self.gen_loyalty_details()

    def gen_user_prefs(self):

        self.gen_ui_theme()
        self.gen_ui_language()
        self.gen_promotion_email()
        self.gen_promotion_category()

    def gen_loyalty_details(self):

        self.gen_loyalty_score()
        self.gen_membership_type()
        self.gen_reward_points()
        self.gen_redeemed_points()
        self.gen_friends_referred()
 
    def gen_first_name(self):
        self.user_profile.first_name = random.choice(self.fn_master_list)

    def gen_last_name(self):
        self.user_profile.last_name = random.choice(self.ln_master_list)

    def gen_display_name(self):
        self.user_profile.display_name = self.user_profile.first_name + " " + self.user_profile.last_name

    def gen_age(self):
        self.user_profile.age = random.randint(15,60)

    def gen_email(self):
        self.user_profile.email = self.user_profile.first_name + "." + self.user_profile.last_name + "@snailmail.com"

    def gen_state(self):
        self.user_profile.state = random.choice(self.state_master_list)

    def gen_user_id(self):
        self.user_profile.user_id = self.user_profile.first_name + "_" + str(random.randint(10, 10000)) + str(random.randint(10, 10000))
        if ( len(self.user_id_master) < 20 ):
            self.user_id_master.append(self.user_profile.user_id)
	
    def gen_document_type(self):
        self.user_profile.doc_type = "user_profile"

    def gen_password(self):
        self.user_profile.password = self.user_profile.first_name + str(random.randint(10,99))

    def gen_lastlogintime(self):
        curr_time = datetime.utcnow()
        time_since_creation = curr_time - self.user_profile.user_creation_time
        time_add = timedelta(days = random.randint( int(time_since_creation.days/2), time_since_creation.days - 1)) 
        self.user_profile.last_login_time = self.user_profile.user_creation_time + time_add
        self.user_profile.last_login_time_str = self.user_profile.last_login_time.ctime()

    def gen_usercreationtime(self):
        curr_time = datetime.utcnow()
        time_lag = timedelta(days = random.randint(5, 1000))
        self.user_profile.user_creation_time = curr_time - time_lag
        self.user_profile.user_creation_time_str = self.user_profile.user_creation_time.ctime()

    def gen_ui_theme(self):
        theme_options = ["Grafitti", "Pebbles", "Planets", "Mountains", "Beach", "Tree Tops", "Ocean", "Wood"]
        self.user_profile.ui_theme = random.choice(theme_options)

    def gen_ui_language(self):
        languages = ["English", "French", "Spanish", "German"]
        self.user_profile.ui_language = random.choice(languages)

    def gen_promotion_email(self):
        promotion_email_pref = [True, False]
        self.user_profile.promotion_email = random.choice(promotion_email_pref)

    def gen_promotion_category(self):
        if self.user_profile.promotion_email:
            promotion_category = ["Books", "Music", "Films"] 
            for i in xrange(random.randint(1, len(promotion_category))):
                self.user_profile.promotion_category.append(promotion_category[i])

    def gen_loyalty_score(self):
        self.user_profile.loyalty_score = random.random() * 10

    def gen_membership_type(self):
        if self.user_profile.loyalty_score > 9:
            self.user_profile.membership_type = "Platinum"
        elif self.user_profile.loyalty_score <= 9 and self.user_profile.loyalty_score > 7:
            self.user_profile.membership_type = "Gold"
        elif self.user_profile.loyalty_score <= 7 and self.user_profile.loyalty_score > 4:
            self.user_profile.membership_type = "Silver"
        else:
            self.user_profile.membership_type = "Basic"

    def gen_reward_points(self):
        self.user_profile.reward_points = random.randint(1,100) * int(self.user_profile.loyalty_score) * 3

    def gen_redeemed_points(self):
        self.user_profile.redeemed_points = random.randint(1,100) * int(self.user_profile.loyalty_score) * 3

    def gen_friends_referred(self):
        referred_delta = 5
        num_users = len(self.user_id_master)
        if (self.user_profile.loyalty_score > referred_delta) and (num_users > referred_delta) :
            for i in xrange(0, random.randint(0, int(self.user_profile.loyalty_score) - referred_delta) ) :
                random_pick = random.randint(0, num_users - 1)
                self.user_profile.friends_referred.append(self.user_id_master[random_pick])
                del self.user_id_master[random_pick]
                num_users = num_users - 1

    def gen_order_history(self):

        for x in xrange(random.randint(0, int(self.user_profile.loyalty_score))):
            order = {}
            order["order_id"] = "T" + str(random.randint(1000, 9999)) + str(random.randint(2000, 7000)) + str(random.randint(1000, 9999))
            user_valid_time = self.user_profile.last_login_time - self.user_profile.user_creation_time
            order_datetime = self.user_profile.user_creation_time + timedelta( days = random.randint(1, user_valid_time.days) )
            order["order_datetime"] = order_datetime.ctime()
            self.user_profile.order_history.append(order)


    def gen_most_searched(self):

        category = {}
        category["Books"] = [ "Biographies", "History", "Humor", "Religion", "Medicine", "NonFiction", "Travel", "Sports & Adventure", "Home & Garden", "Diet & Health", "Children's Books", "Business & Money", "Cookbooks, Food & Wine" ]
        category["Films"] = [ "Action", "Animation", "Foreign Films", "Classic Films", "Comedy", "Documentary", "Drama", "Fitness / Instructional", "Music & Musicals", "Sci-Fi, Fantasy & Horror", "Sports" ]
        category["Music"] = [ "Alternative", "Blues and Folk", "Broadway and Vocal", "Classical Music", "Country Music", "Jazz", "Kid's Music", "New Age", "Opera and Vocal", "Pop Music", "R&B and Rap", "Religious Music", "Rock", "Soundtracks", "World Music" ] 
        searched_count = random.randint(0, len(category.keys()))
        offset = 3
        for k,v in category.items():
           if searched_count > 0:
               searched = {}
               searched["category"] = k
               searched["sub-category"] = []
               for n in xrange(random.randint(1, offset)) :
                   searched["sub-category"].append(v[ (n - 1) * offset + random.randint(0, offset)])
               self.user_profile.most_searched.append(searched)
               searched_count = searched_count - 1
           else:
               break
            
class MemcachedLoader(object):
    
    def __init__(self, serverip = "localhost", port = 11210, bucket = "default", password = ""):
        
        self.client = MemcachedClient(serverip, port)
        self.client.sasl_auth_plain(bucket, password)

    def load_one_json(self, key, doc):

        count = 0 
        loaded = False
        while count < 60 and not loaded:
            try:
                self.client.set(key, 0, 0, doc)
                loaded = True
            except MemcachedError as error:
                if error.status == 134:
                    self.log.error("Memcached error 134, wait for 5 seconds and then try again")
                    count += 1
                    time.sleep(5)


parser = OptionParser()
parser.add_option("-n", "--num_user_profiles", dest="num_user_profiles", type = "int", default = 0,
                  help="Number of JSON User Profiles to be generated")
parser.add_option("-s", "--server", dest="server", default = "localhost",
                  help="Server Hostname/IP address running Couchbase")
parser.add_option("-b", "--bucket", dest="bucket", default = "default",
                  help="Bucket to be loaded with docs")
parser.add_option("-p", "--password", dest="password", default="",
                  help="Password for the bucket")
parser.add_option("-o", "--with_orders", action="store_true", dest="with_orders", default=False,
				  help="Generate Orders for User Profiles(Default is true)")

(options, args) = parser.parse_args()

profile_gen = UserProfileGenerator()
#memcached_loader = MemcachedLoader("175.41.158.100", 11210, "default")
memcached_loader = MemcachedLoader(options.server, 11210, options.bucket, options.password)
for x in xrange(options.num_user_profiles):
    user_profile = profile_gen.create_single_user_profile()
    memcached_loader.load_one_json(user_profile["profile_details"]["user_id"], json.dumps(user_profile))

    if options.with_orders:
        order_gen = OrderGenerator()
        orders = order_gen.generate_orders_from_history(user_profile["order_history"])
        for n in xrange(len(orders)):
            memcached_loader.load_one_json(orders[n]["order_details"]["order_id"], json.dumps(orders[n]))

