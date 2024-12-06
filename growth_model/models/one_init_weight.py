"""
SPDX-FileCopyrightText: 2021 Alfred Wegener Institute Helmholtz Centre for Polar and Marine Research (AWI)
SPDX-License-Identifier: MIT


This file provides a one_init_weight model setup
"""

import time
import pathlib
import logging

import pandas as pd
from growth_model.constants import C_AVG
from growth_model.equations import equation2, equation3


def one_weight(temp: list, weight: float, output: pathlib.Path):
    """
    Compute weight at age of Atlantic cod
    Takes parameters from config file one_weight.toml 

    @param temp: a list of input temperatures (list, °C)
    @param weight: initial weight of individual (single number, g)
    @param output: output directory and file name 
    @author: mbutzin 2015-2018
    @author: nsokolov 2018 - 2022
    @author: arohner 2021 - 2022
    @return:
    """

    # USER INPUTS: input temperature (°C), initial weights (g), output directory
    input_temps = temp
    init_weight = weight

    logging.debug(f'USER TEMPERATURES: {input_temps} °C')
    logging.debug('USER_WEIGHTS: init_weight, g')

    # Initialize a time step
    # For example, if you calculate growth over 3 days -> dt = 3
    dt = 1

    # Create an empty data frame to save the utput values
    df = pd.DataFrame(columns=['Input_Temp', 'a', 'b', 'Growth_Rate', 'Final_Weight'])
    df['Input_Temp'] = input_temps
    df = df.set_index('Input_Temp')

    # Record starting time for calculations
    begin_time = time.time()

    # Start calculations

    temp_count = 1
    for each_input_temp in input_temps:
        logging.debug(f'Temperature value {temp_count} each_input_temp °C')
        # Calculate a (Eg.2 in Butzin and Poertner, 2016)
        a = equation2(each_input_temp)
        # Calculate b (Eq.3 in Butzin and Poertner, 2016)
        b = equation3(each_input_temp)
        # Calculate relative growth rate
        growth_rate = 0.01 * (a * init_weight ** b - C_AVG)
        # Calculate weight (g)
        end_weight = init_weight * (1. + dt * growth_rate)
        # Add calculated values to the DataFrame
        df.loc[[each_input_temp], ['a']] = a
        df.loc[[each_input_temp], ['b']] = b
        df.loc[[each_input_temp], ['Growth_Rate']] = growth_rate
        df.loc[[each_input_temp], ['Final_Weight']] = end_weight
        # Calculations finished
        logging.debug(f'a = {round(a, 3)} % per day / day ^ 1/b')
        logging.debug(f'b = {round(b, 3)}')
        logging.debug(f'growth_rate = {round(growth_rate, 3)} % per unit time')
        logging.debug(f'end_weight = {round(end_weight, 3)} g')
        temp_count = temp_count + 1
    logging.debug(f'{df}')
    if not output.parent.exists():
        output.parent.mkdir(parents=True)
    # Save DataFrame to csv
    df.to_csv(output)
    logging.info(f'Saved results to {output.resolve()}')
    # Record final time when calculations are finished
    finish_time = time.time()
    # Calculate duration of calculations
    calc_time = finish_time - begin_time
    logging.debug(f'Calculated over time: {calc_time} seconds')
    return None
