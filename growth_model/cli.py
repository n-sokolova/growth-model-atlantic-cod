"""
SPDX-FileCopyrightText: 2021 Alfred Wegener Institute Helmholtz Centre for Polar and Marine Research (AWI)
SPDX-License-Identifier: MIT


Functions in this file take information from a command line user input and parameters from config .toml file 
"""

import argparse
import sys
import pathlib
import logging

from growth_model.utils import init_logger
from growth_model.models.base import base
from growth_model.models.one_temp_input import one_temp
from growth_model.models.one_init_weight import one_weight
from growth_model.models.one_dim import one_dim
from growth_model.models.multi_dim import multi_dim
from growth_model.utils import load_config


def _parse_args():
    """
    Parsing the commandline arguments

    @return: the parsed arguments (argparse.Namespace)
    """

    parser = argparse.ArgumentParser(description='Estimates  growth-rate per day and the weight of atlantic cod',
                                     formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('config_file', type=str,
                        help='Configuration file (.toml) - contains model and settings for '
                             'running the calculation')

    parser.add_argument('output', type=str,
                        help='Output where calculation results are stored. '
                             'Destination will be created if it does not exist, existing files will be overwritten.\n'
                             'For models "base", "one_dim", "one_temp" and "one_weight" the output is a CSV-File\n'
                             'For model "multi_dim" the output is a directory, where results are stored as NC-files')
    return parser.parse_args()


def main():
    """
    Entrypoint of the command line interface for interacting with  cod-growth-models

    @return: exit code
    """

    # Initialize logger
    logger_config = pathlib.Path.cwd().joinpath('logger.conf')
    init_logger(logger_config)

    # Parse cli arguments
    args = _parse_args()
    settings = load_config(args.config_file)

    model = settings['model']
    output = pathlib.Path(args.output)

    models_output_dir = ['multi_dim']
    models_output_file = ['base', 'one_dim', 'one_temp', 'one_weight']

    if model in models_output_dir and output.is_file():
        sys.exit(f'Error: Output must be directory for models {models_output_dir}')
    if model in models_output_file and output.is_dir():
        sys.exit(f'Error: Output must be a file for models {models_output_file}')

    if model == 'base':
        logging.info('Calculating growth model with model "base"...')
        try:
            base(temp=settings['temp'], weight=settings['weight'], output=output)
        except KeyError:
            sys.exit(f'Error: Model-Settings for model "base" in config-file {args.config_file} are incomplete!')

    elif model == 'one_dim':
        logging.info('Calculating growth model with model "one_dim"...')
        try:
            one_dim(min_temp=settings['min_temp'], max_temp=settings['max_temp'], temp_step=settings['temp_step'],
                    weight=settings['weight'], max_age=settings['max_age'], output=output)
        except KeyError:
            sys.exit(f'Error: Model-Settings for model "one_dim" in config-file {args.config_file}'
                     f' are incomplete!')

    elif model == 'one_temp':
        logging.info('Calculating growth model with model "one_temp"...')
        try:
            one_temp(temp=settings['temp'], weight=settings['weight'],
                     output=output)
        except KeyError:
            sys.exit(f'Error: Model-Settings for model "one_temp" in config-file {args.config_file} are incomplete!')

    elif model == 'one_weight':
        logging.info('Calculating growth model with model "one_weight"..')
        try:
            one_weight(temp=settings['temp'], weight=settings['weight'],
                       output=output)
        except KeyError:
            sys.exit(f'Error: Model-Settings for model "one_weight" in config-file {args.config_file} are incomplete!')

    elif model == 'multi_dim':
        logging.info('Calculating growth model with model "multi_dim"...')
        try:
            multi_dim(lat=settings['lat'], lon=settings['lon'], depth=settings['depth'],
                      max_age=settings['max_age'], first_year=settings['first_year'],
                      final_year=settings['final_year'], exp_name=settings['exp_name'],
                      region=settings['region'], input_data=settings['input_data'], output=output)
        except KeyError:
            sys.exit('Error: model "multi_dim" expects parameter-settings!')
    else:
        logging.critical(f'Error: model "{model}" not available')
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
