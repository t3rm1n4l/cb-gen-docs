
import random

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
