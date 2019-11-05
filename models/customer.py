from numpy import random
import configparser
import json
import logging


class Customer():

    def __init__(self, config, cur_month, id):

        # INIT
        self.spending_growth_rate = float(config["spending_growth_rate"])
        self.no_employees_with_cards = abs(int(random.normal(loc=int(config["av_no_employees_with_cards"]), scale=float(config["dev"]))))
        self.max_spend = int(config["max_spend"])
        self.spend_stddev = float(config["spend_stddev"])
        self.irs = json.loads(config["monthly_ir"])

        self.monthly_spend = {0: 0}
        self.cur_month = cur_month
        self.average_spend = self.set_average_spend(float(config["average_spend"]))
        self.id = id
        self.config = config

        self.defaulted = False

    def __repr__(self):
        return str(self.id) + " customer with average_spend " + str(self.average_spend) + " and is default: " + str(self.defaulted)

    def set_average_spend(self, customer_av_spend):
        if self.cur_month == 0:
            return customer_av_spend
        else:
            ir_diff = float(self.irs[self.cur_month-1]) - float(self.irs[self.cur_month])
            next_spend = customer_av_spend + (ir_diff*customer_av_spend*0.2) # 1 decimal change in IR changes av spend by 5%
            return next_spend * self.spending_growth_rate # companies growing and spending more.


    def determine_next_month_spend(self, recession_bool):
        self.average_spend = self.set_average_spend(self.average_spend)
        if self.spend_stddev < self.average_spend/2:
            self.spend_stddev *= float(self.config["std_growth_rate"])
        if recession_bool:
            # 0.7 spending
            sample = random.normal(loc=(self.average_spend*0.7), scale=self.spend_stddev)
        else:
            sample = random.normal(loc=self.average_spend, scale=self.spend_stddev)
        if sample < 0:
            # otherwise default OR stopped being customer and signal removal of client....
            self.monthly_spend[self.cur_month] = 0
            self.defaulted = True
            return True
        else:
            if sample > self.max_spend:
                self.monthly_spend[self.cur_month] = self.max_spend
            else:
                self.monthly_spend[self.cur_month] = sample
            return False

    def advance_month(self, recession):
        if not self.defaulted:
            defaulted = self.determine_next_month_spend(recession)
            # print(str(self.id) + "spend for month ", self.cur_month, " is ", str(self.monthly_spend[self.cur_month]))#, " and self ", self.average_spend)
            # logging.info("now average_spend is " + str(self.monthly_spend[self.cur_month]))
            self.cur_month += 1
            return defaulted
        else:
            # print(str(self.id), " defaulted 0")
            self.monthly_spend[self.cur_month] = 0
            self.cur_month += 1
            return False
