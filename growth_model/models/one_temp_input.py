"""
SPDX-FileCopyrightText: 2021 Alfred Wegener Institute Helmholtz Centre for Polar and Marine Research (AWI)
SPDX-License-Identifier: MIT


This file provides a one_input_temp model setup
"""

import time
import logging
import pathlib

import pandas as pd
from growth_model.constants import C_AVG
from growth_model.equations import equation2, equation3


def one_temp(temp: float, weight: list, output: pathlib.Path):
    """
    Calculate growth of Atlantic cod using input temperature and initial weight

    @param temp: input temperature (single values, °C)
    @param weight: a list of initial weights (g)
    @param output: output destination
    @author: nsokolov 2018 - 2022
    @author: arohner 2021 - 2022
    @return: None
    """

    # Define the path to the growth models functions and constants

    # USER INPUTS: input temperature (°C), initial weights (g), output directory
    input_temp = temp
    init_weights = weight

    logging.debug(f'USER TEMPERATURES: {input_temp} °C')
    logging.debug(f'USER_WEIGHTS: {init_weights} g')

    # Initialize a time step 
    # For example, if you calculate growth over 3 days -> dt = 3
    dt = 1

    # Create an empty data frame to save the utput values
    df = pd.DataFrame(columns=['Init_Weight', 'a', 'b', 'Growth_Rate', 'Final_Weight'])
    df['Init_Weight'] = init_weights
    df = df.set_index('Init_Weight')

    # Record starting time for calculations
    begin_time = time.time()

    # Start calculations

    # Parameters a and b are independent of initial weight
    # Calculate a (Eg.2 in Butzin and Poertner, 2016)
    a = equation2(input_temp)
    # Calculate b (Eq.3 in Butzin and Poertner, 2016)
    b = equation3(input_temp)

    weight_count = 1
    for each_init_weight in init_weights:
        logging.debug(f'Weight value {weight_count} = {each_init_weight} g')
        # Calculate relative growth rate 
        growth_rate = 0.01 * (a * each_init_weight ** b - C_AVG)
        # Calculate weight (g)
        end_weight = each_init_weight * (1. + dt * growth_rate)
        # Add calculated values to the DataFrame
        df.loc[[each_init_weight], ['a']] = a
        df.loc[[each_init_weight], ['b']] = b
        df.loc[[each_init_weight], ['Growth_Rate']] = growth_rate
        df.loc[[each_init_weight], ['Final_Weight']] = end_weight
        # Calculations finished
        logging.debug(f'a = {round(a, 3)} % per day / day ^ 1/b')
        logging.debug(f'b = {round(b, 3)}')
        logging.debug(f'growth_rate = {round(growth_rate, 3)} % per unit time')
        logging.debug(f'end_weight = {round(end_weight, 3)} g')
        weight_count = weight_count + 1
    logging.debug(df)
    if not output.parent.exists():
        output.parent.mkdir(parents=True)
    df.to_csv(output)
    logging.info(f'Saved results to {output.resolve()}')
    # Record final time when calculations are finished
    finish_time = time.time()
    # Calculate duration of calculations
    calc_time = finish_time - begin_time
    logging.debug(f'Calculated over time: {round(calc_time, 3)} seconds')
    return None
