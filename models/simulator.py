import matplotlib.pyplot as plt
import numpy as np
import logging
import os


class Simulator():

    def __init__(self, no_experiments, no_months, log_name):
        self.no_months = no_months
        self.no_experiments = no_experiments
        self.average_profits = np.zeros(no_months)

        # for handler in logging.root.handlers[:]:
        #     logging.root.removeHandler(handler)
        #
        # # logging
        # if os.path.exists(log_name):
        #     os.remove(log_name)
        # filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "logs", "simulator"+log_name)
        # logging.basicConfig(level=logging.INFO, format='', filename=filename)
        # logging.info('STARTING Simulator')

    def relevant_stats(self, profit, capital, month):

        #TODO set numbers
        if profit < -1000000:
            logging.info("ALERT PROFIT IS LOW @ " + str(profit))

        if capital < -10000000:
            logging.info("CAPITAL PROFIT IS LOW @ "+ str(capital))

        # print(month, profit, capital)


    def aggregate_plot(self, month, profit):
        self.average_profits[month] += profit

    def plot(self):
        self.average_profits = list(self.average_profits/self.no_experiments)
        plt.plot(range(self.no_months), self.average_profits)
        plt.show()
