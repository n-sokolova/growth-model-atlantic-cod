"""
SPDX-FileCopyrightText: 2021 Alfred Wegener Institute Helmholtz Centre for Polar and Marine Research (AWI)
SPDX-License-Identifier: MIT


This file provides a one_dim model setup
"""

import numpy as np
import pandas as pd
import pkgutil
import pathlib
import logging

from io import BytesIO


def one_dim(min_temp: float, max_temp: float, temp_step: float,
            weight: int, max_age: int, output: pathlib.Path):
    """

    @param min_temp: minimum temperature in an experiment temperature range (°C)
    @param max_temp: maximum temperature in an experiment temperature range (°C)
    @param temp_step: temperature step in an experiment (°C)
    @param weight: initial weight of individual (g)
    @param max_age: maximum age of individual (years)
    @param output: output file (pathlib.Path)
    @author: mbutzin 2015-2018
    @author: nsokolov 2018 - 2022
    @author: arohner 2021 - 2022

    @return: None
    """

    data = BytesIO(pkgutil.get_data(__name__, '../data/growth_parameters_multistep.npz'))
    growth_params = np.load(data)

    ages = np.arange(1, max_age * 365)
    a_fit = growth_params['a_fit']  # the original temperature increment
    b_fit = growth_params['b_fit']  # underlying a_fit and b_fit is 0.1 K
    c_avg = growth_params['c_avg']

    temp_range = np.arange(float(min_temp), float(max_temp), float(temp_step))  # Temperature range in °C

    weight_at_age = np.zeros((max_age * 365, len(temp_range)))  # weight at age (in g) for a given temperature range
    weight_at_age[0, :] = weight  # initial weight in g
    dt = 1  # time step in days

    i_temp = 0  # temperature index, initial value

    # loop over temperatures, increasing values by 0.5°C
    for _ in temp_range:
        for age in ages:
            growth_rate = 0.01 * (a_fit[i_temp] * weight_at_age[age - 1, i_temp] ** b_fit[i_temp] - c_avg)
            weight_at_age[age, i_temp] = weight_at_age[age - 1, i_temp] * (1. + dt * growth_rate)
        i_temp = i_temp + 1
    df = pd.DataFrame(weight_at_age, columns=temp_range)
    df.index.name = 'day'
    if not output.parent.exists():
        output.parent.mkdir(parents=True)
    df.to_csv(output)
    logging.info(f'Saved results to {output.resolve()}')
    logging.debug(f'{df}')
    return None
