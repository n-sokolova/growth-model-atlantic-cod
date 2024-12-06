"""
SPDX-FileCopyrightText: 2021 Alfred Wegener Institute Helmholtz Centre for Polar and Marine Research (AWI)
SPDX-License-Identifier: MIT


This file provides a multi_dim model setup
"""


import warnings
import pathlib
import logging

import numpy as np
import pandas as pd
import xarray as xr

from growth_model.constants import C_AVG
from growth_model.equations import equation2, equation3
from growth_model.utils import save_netcdf


def multi_dim(lat: list, lon: list, depth: list,
              max_age: int, first_year: int, final_year: int,
              exp_name: str, region: str, input_data: str, output: pathlib.Path):
    """
    Compute weight-at-age of Atlantic cod using multidimensional ocean temperature data.

    @param lat: latitude (as a list of floating numbers)
    @param lon: longitude (as a list of floating numbers)
    @param depth: depth levels (as a list of floating numbers)
    @param max_age: maximum age of fish (in years)
    @param first_year: first year in the input dataset
    @param final_year: last yera in the input dataset
    @param exp_name: experiment name (e.g. related to the name of the input dataset)
    @param region: region name (e.g. Celtic Sea)
    @param input_data: input folder (reads *.nc - files)
    @param output: ouput folder 
    @author: nsokolov 2018 - 2022
    @author: arohner 2021 - 2022
    @return: None
    """

    # Define time series
    years = np.arange(first_year, final_year + 1)

    # Number of years in one life cycle of an individual cod species
    generation = max_age

    # Initial time step (by default = 1 day)
    dt = 1

    # Get temperature files from input directory
    my_files = input_data + '/*.nc'
    input_files = xr.open_mfdataset(my_files, decode_times=False)
    logging.debug(f'DATA SET: {input_files}')
    # Create new_time for the dataset to change it from 360_d to standard calendar
    # Check your netcdf files which calender they have
    new_time = pd.date_range(str(first_year) + '-01-01', str(final_year + 1) + '-01-01', freq='M')

    # You need new times in you dataset
    # Only if you have other than standard calendar
    input_files = input_files.assign_coords({'time': new_time})

    # Define dimensionality of coords
    length_depth = len(depth)
    length_lat = len(lat)
    length_lon = len(lon)

    # Start calculations
    for each_year in years:
        initial_year = each_year
        logging.debug(f'INITIAL YEAR: {initial_year}')
        # Identifiyng the last year (death of cod)
        last_year = initial_year + generation
        logging.debug(f'LAST YEAR: {last_year}')
        # Beginning of life cycle
        age = 1
        weight = np.ones(shape=(length_depth, length_lat * length_lon), dtype='f')
        growth_rates = np.zeros(shape=(length_depth, length_lat * length_lon), dtype='f')
        for year in range(initial_year, last_year):
            logging.debug(f'WORK ON YEAR: {year}')
            if last_year > years[-1]:
                logging.debug('YEAR IS NOT IN DATA SET')
                break
            else:
                my_temp = input_files.thetao.sel(time=str(year), depth_coord=depth, latitude=lat, longitude=lon)
                logging.debug(my_temp)
                # Partly vectorize 4D temperature fields to accelerate the computations
                temp_input_3d = my_temp.values.reshape(12, length_depth, length_lat * length_lon)
                # Set NaN values
                temp_input_3d[np.where(temp_input_3d[:, :, :] <= -998)] = np.nan
                # Initialize necessary variable fields
                a = np.zeros(shape=(length_depth, length_lat * length_lon), dtype='f')
                b = np.zeros(shape=(length_depth, length_lat * length_lon), dtype='f')
                for mon in np.arange(0, 12):
                    for _ in np.arange(0, 30):
                        for i in np.arange(0, length_depth):
                            a[i, :] = equation2(temp_input_3d[mon, i, :])
                            b[i, :] = equation3(temp_input_3d[mon, i, :]) * (-1.)
                            growth_rates[i, :] = 0.01 * (a[i, :] * weight[i, :] ** b[i, :] - C_AVG)
                            growth_rates[i, :] = np.where(growth_rates[i, :] < 0, 0, growth_rates[i, :])
                            weight[i, :] = weight[i, :] * (1. + dt * growth_rates[i, :])
                new_year = int(year) + 1
                # Reshape data to original shape
                a_3d = a.reshape(length_depth, length_lat, length_lon)
                b_3d = b.reshape(length_depth, length_lat, length_lon)
                growth_rates_3d = growth_rates.reshape(length_depth, length_lat, length_lon)
                # 3D field with asymptotic weight

                weight_3d = 0.001 * weight.reshape((length_depth, length_lat, length_lon))
                # Calculate maximum asymptotic weight at a given location ->  ("W*" in Butzin and Pörtner (2016))
                with warnings.catch_warnings():
                    warnings.simplefilter('ignore')
                    weight_max = np.nanmax(weight_3d, axis=0)

                # Create output directories if they do not exist
                output_dir = output.joinpath(exp_name, region)
                logging.debug(f'MY OUTPUT FOLDER: {output_dir}')
                output_a_3d = output_dir.joinpath('a_3d')
                output_b_3d = output_dir.joinpath('b_3d')
                output_growth_rates_3d = output_dir.joinpath('growth_rates_3d')
                output_weight_3d = output_dir.joinpath('weight_3d')
                output_weight_max = output_dir.joinpath('weight_max')

                output_pathlist = [
                    output_a_3d,
                    output_b_3d,
                    output_growth_rates_3d,
                    output_weight_3d,
                    output_weight_max
                ]
                for f in output_pathlist:
                    if not f.exists():
                        f.mkdir(parents=True)

                # Save netcdf (a_3d, b_3d, growth_rates_3d, weight_3d, weight_max)
                save_netcdf(
                    data=a_3d, var_name='a_3d', directory=output_a_3d,
                    year=new_year, age=age, depths=depth, lat=lat, lon=lon
                )
                save_netcdf(
                    data=b_3d, var_name='b_3d', directory=output_b_3d,
                    year=new_year, age=age, depths=depth, lat=lat, lon=lon
                )
                save_netcdf(
                    data=growth_rates_3d, var_name='growth_rates_3d', directory=output_growth_rates_3d,
                    year=new_year, age=age, depths=depth, lat=lat, lon=lon
                )
                save_netcdf(
                    data=weight_3d, var_name='weight_3d', directory=output_weight_3d,
                    year=new_year, age=age, depths=depth, lat=lat, lon=lon
                )
                save_netcdf(
                    data=weight_max, var_name='weight_max', directory=output_weight_max,
                    year=new_year, age=age, depths=depth, lat=lat, lon=lon,
                    dimension_labels=('latitude', 'longitude')
                )
                age = age + 1
    logging.info(f'Saved results to folder {output.resolve()}')
    return None
