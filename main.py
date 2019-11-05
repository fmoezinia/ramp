#!/usr/bin/env python

from models.core_ramp import RampCore
from models.customer import Customer
from models.simulator import Simulator

import configparser





def main_one_ramp():

    config = configparser.ConfigParser()
    config.read('configs/config.ini')

    


    ramp_config = config['RAMPCORE']
    customer_config = config['CUSTOMERS']
    general_config = config['GENERAL']
    months = int(general_config['number_of_months'])
    log_file_name = str(general_config['log_file_name'])

    # initialize Ramp and Client
    ramp = RampCore(ramp_config, customer_config, log_file_name)

    print("SIMULATING ", months, " months forward")
    for i in range(months):
        ramp.advance_month()


def main_experiment():

    config = configparser.ConfigParser()
    config.read('configs/config.ini')
    ramp_config = config['RAMPCORE']
    customer_config = config['CUSTOMERS']
    general_config = config['GENERAL']
    months = int(general_config['number_of_months'])
    log_file_name = str(general_config['log_file_name'])

    # initialize Ramp and Client
    ramp = RampCore(ramp_config, customer_config, log_file_name, simulating=True)

    no_experiments = int(general_config['no_experiments'])
    simulator = Simulator(no_experiments, months, log_file_name)

    print("SIMULATING ", months, " months forward")
    for i in range(no_experiments):
        for j in range(months):
            profit, capital = ramp.advance_month()
            simulator.relevant_stats(profit, capital, j)
            simulator.aggregate_plot(j, profit)
        ramp = RampCore(ramp_config, customer_config, log_file_name, simulating=True)


    simulator.plot()

#main_experiment()




############### MAIN ################

simulator = True
if simulator:
    main_experiment()
else:
    main_one_ramp()
