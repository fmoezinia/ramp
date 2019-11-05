from .customer import Customer
from .growth import logistic_growth
from functools import reduce

import logging
import os
import math
import random


class RampCore():


    def __init__(self, ramp_config, customer_config, log_name, simulating=False):

        # init
        self.cur_month = 0
        self.current_customers = [] # includes defaulted customers
        self.customer_config = customer_config
        self.ramp_config = ramp_config

        # state maintenance
        self.revenues = {0: 0}
        self.profits = {0: 0}
        self.seq_id = 0

        # configs
        self.capital = {0: int(ramp_config["inital_capital"])}
        self.number_clients = {0: int(ramp_config["initial_no_clients"])}
        self.total_monthly_cost = {0: float(ramp_config["intial_monthly_costs"])} # more breakdown? people/office space probably 1? marqeta? visa?
        self.cost_growth_rate = float(ramp_config["cost_growth_rate"])
        self.interchange_fee = float(ramp_config["interchange_fee"]) # that Ramp charges
        self.tax_rate = float(ramp_config["tax_rate"])
        self.price_per_card_month = float(ramp_config["price_per_card_month"])
        self.prob_recession = float(ramp_config["prob_recession"])
        self.growth_type = str(ramp_config["growth_type"])
        self.simulating = simulating
        if not simulating:
            # logging
            if os.path.exists(log_name):
                print('removing file')
                os.remove(log_name)
            filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'logs', log_name)
            logging.basicConfig(level=logging.INFO, format='', filename = filename)
        else:
            if os.path.exists(log_name):
                os.remove(log_name)
            filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "logs", "simulator"+log_name)
            logging.basicConfig(level=logging.INFO, format='', filename=filename)
            logging.info('STARTING Simulator')

    def get_number_current_clients(self):
        return len(self.current_customers)

    def _calculate_revenue(self, monthly_spend, no_cards):
        # sets revenue for current month (IFC * spend)
        #TODO add dyanmic pricing for no cards?
        ifc_rev = monthly_spend*self.interchange_fee
        physical_card_rev = no_cards * self.price_per_card_month
        return ifc_rev + physical_card_rev

    def _set_revenue_then_profit(self):
        logging.info("Setting revenue for month " + str(self.cur_month))
        revenue = reduce((lambda x, y : x+y), [(self._calculate_revenue(client.monthly_spend[self.cur_month], client.no_employees_with_cards)) for client in self.current_customers])
        self.revenues[self.cur_month] = revenue
        logging.info("now revenue is " + str(self.revenues[self.cur_month]))

        self._update_costs()
        return self._set_profit()


    def _set_profit(self):
        # sets profit for current month
        pre_tax = self.revenues[self.cur_month] - self.total_monthly_cost[self.cur_month]
        if pre_tax < 0:
            # no taxable income
            self.profits[self.cur_month] = pre_tax
        else:
            self.profits[self.cur_month] = pre_tax*(1-self.tax_rate)
        logging.info("Now Profit is " + str(self.profits[self.cur_month]))
        return self.profits[self.cur_month]

    def _update_costs(self):
        self.total_monthly_cost[self.cur_month] = self.total_monthly_cost[self.cur_month-1]*self.cost_growth_rate
        logging.info("Now Costs are " + str(self.total_monthly_cost[self.cur_month]))
        # TODO loss if a co defaults on credit.


    def init_new_customers(self):
        logging.info("INIT new customers")
        if self.cur_month not in self.number_clients:
            if self.growth_type == "logistic":
                next_no_clients = int(logistic_growth(self.cur_month))
            elif self.growth_type == "geometric":
                next_no_clients = math.floor(self.number_clients[self.cur_month-1] * float(self.ramp_config["client_base_growth_rate"]))
            logging.info(str(next_no_clients) + " total customers in the next month")
            self.number_clients[self.cur_month] = next_no_clients
        new_clients = self.number_clients[self.cur_month]-self.get_number_current_clients() # for last month (len customers)
        # print(new_clients, ' new cs')
        logging.info("adding " + str(new_clients) + " clients this month")
        for i in range(new_clients):
            self.current_customers.append(Customer(self.customer_config, self.cur_month, self.seq_id))
            self.seq_id += 1

    def recess(self):
        rando_float = random.random() # 0 to 1
        if rando_float < self.prob_recession:
            return True
        return False


    def advance_month(self):
        if not self.simulating:
            print("------------- month ", str(self.cur_month), "-------------")
            print("----------------------------------------------")

        self.cur_month += 1
        logging.info("\n ADVANCE ONE MONTH to " + str(self.cur_month))
        # modify customer base
        self.init_new_customers()


        recession_bool = self.recess()
        if recession_bool:
            logging.info("RECESSION HAS HIT")

        for client in self.current_customers:
            default_bool = client.advance_month(recession_bool)
            if default_bool:
                logging.info("client defaulted!")

        #TODO capital
        # collect resulting spend + other data
        return self._set_revenue_then_profit(), self.capital[0]
