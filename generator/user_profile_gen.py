
import random
import os
from datetime import datetime, timedelta


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

class UserProfileGenerator(object):

    def __init__(self, mutation_mode):

        self.fn_master_list = []
        self.ln_master_list = []
        self.state_master_list = []
        self.user_id_master = []

        self.read_master_data()     

        self.generated_profile_count = 0
        self.mutation_mode = mutation_mode
        self.mutation_list = []

    def get_mutation_list(self):
        return self.mutation_list

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
            self.fn_master_list = line.strip().split(',')

        fn_file_handle.close()

        if not os.path.exists(LAST_NAME_FILE):
            print "LAST NAME DATA FILE IS MISSING. EXITTING!!!"
            exit(-1)

        ln_file_handle = open(LAST_NAME_FILE)
        for line in ln_file_handle:
            self.ln_master_list = line.strip().split(',')

        ln_file_handle.close()

        if not os.path.exists(STATE_NAME_FILE):
            print "STATE NAME DATA FILE IS MISSING. EXITTING!!!"
            exit(-1)

        state_file_handle = open(STATE_NAME_FILE)
        for line in state_file_handle:
            self.state_master_list = line.strip().split(',')

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

        user_profile_map["shipped_order_history"] = self.user_profile.order_history
 
        if len(self.user_profile.most_searched):
            user_profile_map["search_history"] =  self.user_profile.most_searched
 
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
        self.generated_profile_count += 1
        if ( len(self.user_id_master) < 20 ):
            self.user_id_master.append(self.user_profile.user_id)

        if self.mutation_mode > 0  and self.generated_profile_count < 10000:
            self.mutation_list.append(self.user_profile.user_id)

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
                random_pick = random.randint(0, num_users - 2)
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
               num_subcategory = random.randint(1, offset)
               for n in xrange(num_subcategory):
                   searched["sub-category"].append(v[ n * offset + random.randint(1, offset)])
               self.user_profile.most_searched.append(searched)
               searched_count = searched_count - 1
           else:
               break

