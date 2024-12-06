"""
SPDX-FileCopyrightText: 2021 Alfred Wegener Institute Helmholtz Centre for Polar and Marine Research (AWI)
SPDX-License-Identifier: MIT


This file provides the base model setup
"""

import time
import pathlib
import logging

import pandas as pd

from growth_model.equations import equation2, equation3
from growth_model import constants


def base(temp: float, weight: float, output: pathlib.Path, dt=1):
    """
    Base model for calculating growth rate of Atlantic cod (Gadus morua)
    The growth model calculates relative growth per day and final weight (g)
    The model is temperature- and size-dependent
    As inputs it takes environmental temperature and initial weight of individual  

    @param temp: input temperature for growth rate calculation (°C)
    @param weight: initial weight for growth rate calculation (g)
    @param output: output folder for storing calculation result
    @param dt: time step (e.g. if you calculate growth over 3 days -> dt = 3)
    @author: mbutzin 2015 - 2018
    @author: nsokolova 2018-2022
    @author: arohner 2021-2022
    @return: 
    """

    logging.info(f'Initial weight: {weight} g')
    logging.info(f'Input temperature: {temp} °C')

    # Record starting time for calculations
    begin_time = time.time()

    # Calculate a (Eq.2 in Butzin and Poertner, 2016)
    a = equation2(temp)

    # Calculate b (Eg.3 in Butzin and Poertner, 2016)
    b = equation3(temp) * (-1.0)

    # Calculate relative growth rate
    growth_rate = 0.01 * (a * weight ** b - constants.C_AVG)

    # Calculate weight (g)
    final_weight = weight * (1.0 + dt * growth_rate)

    # print model results
    logging.info(f'Relative growth rate: {growth_rate.round(7)} per day')  # round the value to the first 5 decimals
    logging.info(f'Calculated weight: {round(final_weight, 5)} g')  # round the value to the first 5 decimals
    
    # Record final time when calculations are finished
    finish_time = time.time()
    
    # Calculate duration of calculations
    calc_time = finish_time - begin_time
    logging.info(f'Calculated over time: {round(calc_time, 3)} seconds')
    
    # Create an empty data frame to save the output values
    df = pd.DataFrame(index=['output'])
    df['init_weight'] = weight
    df['input_temp'] = temp
    df['a'] = a
    df['b'] = b
    df['growth_rate'] = growth_rate.round(3)
    df['final_weight'] = final_weight

    if not output.parent.exists():
        output.parent.mkdir(parents=True)
    # Save the data frame to csv
    df.to_csv(output)
    logging.info(f'Saved results to {output.resolve()}')
