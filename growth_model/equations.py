"""
SPDX-FileCopyrightText: 2021 Alfred Wegener Institute Helmholtz Centre for Polar and Marine Research (AWI)
SPDX-License-Identifier: MIT


In this file functions for coefficients a and b are defined (Eq. 2 and 3 in Butzin and Poertner, 2016)
"""

from growth_model.constants import A_R, THETA_A, T_R, THETA_H, T_H, B_R, THETA_B, T0

from numpy import exp


def equation2(input_temp):
    """
    This function calculates parameter "a" (Eg. 2 in Butzin and Poertner, 2016)
    This is a nonlinear master reaction model of poikilotherm development 
    with growth inhibition at higher temperatures.

    @param input_temp: input temperature for growth rate calculation (°C)
    @return: a
    """
    temperature_kelvin = input_temp + T0
    # Calculate a
    a_numerator = A_R * exp(THETA_A / T_R - THETA_A / temperature_kelvin)
    a_denominator = 1 + exp(THETA_H / T_H - THETA_H / temperature_kelvin)
    a = a_numerator / a_denominator
    return a


def equation3(input_temp):
    """
    This function calculates an allometric scaling exponent "b" 
    (Arrhenius equation, Eg. 3 in Butzin and Poertner, 2016)

    @param input_temp: input temperature for growth rate calculation (°C)
    @return: b
    """
    temperature_kelvin = input_temp + T0
    # Calculate b
    b = B_R * exp(THETA_B / T_R - THETA_B / temperature_kelvin)
    return b
