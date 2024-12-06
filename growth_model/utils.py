"""
SPDX-FileCopyrightText: 2021 Alfred Wegener Institute Helmholtz Centre for Polar and Marine Research (AWI)
SPDX-License-Identifier: MIT


This file provides supporting functions:
- loading parameters from a config file
- saving the multi_dim model output
"""

import xarray as xr
import tomli
import pathlib
import logging
import sys
import configparser

from logging import config as logging_config


def load_config(config_file):
    """
    Load configuration file (in toml-format) with model-settings
    @param config_file: configuration-file with different model-settings (see documentation for details)
    @return: dict with settings
    """
    with open(config_file, 'rb') as f:
        config = tomli.load(f)
    return config['model_settings']


def save_netcdf(data, var_name, directory: pathlib.Path, year, age, depths, lat, lon,
                dimension_labels=("depth_coord", "latitude", "longitude")):
    """
    Save data in netCDF4 format

    @param data: output data (xarray)
    @param var_name: variable name
    @param directory: output directory
    @param year: specific year in a time series
    @param age: age of individual (years)
    @param depths: ocean depth (kg)
    @param lat: latitude
    @param lon: longitude
    @param dimension_labels: dimension labels
    @return: None
    """
    if "depth_coord" in dimension_labels:
        coordinates = [('depth_coord', depths),
                       ('latitude', lat),
                       ('longitude', lon)]

    else:
        coordinates = [('latitude', lat),
                       ('longitude', lon)]

    da = xr.DataArray(data, dims=dimension_labels, coords=coordinates,
                      name=var_name)

    suffix = str(year) + '_' + var_name + '_' + 'age' + str(age) + '.nc'
    filename = directory.joinpath(suffix)

    da.to_netcdf(filename)


def init_logger(logger_config: pathlib.Path):
    """
    Initialize root logger based on configuration file

    @param logger_config: logger configuration file
    @return: None
    """
    try:
        logging_config.fileConfig(logger_config)
    except (KeyError, configparser.Error) as error:
        print(f'Cannot use default-logger. Reason: {error}')
        print('Use a console logger instead. ')
        logging.root.addHandler(logging.StreamHandler(sys.stdout))
        logging.root.setLevel(logging.INFO)
