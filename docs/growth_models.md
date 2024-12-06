<!--
SPDX-FileCopyrightText: 2021 Alfred-Wegener-Institut, Helmholtz-Zentrum für Polar- und Meeresforschung (AWI)

SPDX-License-Identifier: MIT
-->

# Overview of Growth Model Versions
|Model|Description|Config|Inputs|Outputs|
|-----|-----|-----|-----|-----|
|[` base.py`](./growth_model/models/base.py)| a dimensionless model that calculates relative growth rate and final weight of one individual considering one constant temperature environment | [`base.toml`](./config/base.toml) | temperature: single value (integer), initial weight: single value (integer) |relative growth rate: single value, final weight: single value, file format: csv | 
|[`one_temp_input.py`](./growth_model/models/one_temp_input.py)| a dimensionless model that calculates relative growth rate and final weight of several individuals considering one constant temperature environment |  [`one_temp_input.toml`](./config/one_temp_input.toml)| emperature: single value (integer), initial weight: several values (list) | relative growth rates: list, final weights: list, file format: csv | 
|[`one_init_weight.py`](./growth_model/models/one_init_weight.py)| a dimensionless model that calculates relative growth rate and final weight of one individuals considering several constant temperature environments | [`one_init_weight.toml`](./config/one_init_weight.toml) | temperature: several values (list), initial weight: one value (integer)| relative growth rates: list, final weights: list, file format: csv | 
|[`one_dim.py`](./growth_model/models/one_dim.py)| a 1-dimensional model that calculates continuous growth of several individuals over a given time period under several constant temperature regimes (Fig. 2b in [Butzin and Pörtner, 2016](https://doi.org/10.1111/gcb.13375)). | [`one_dim.toml`](./config/one_dim.toml) | temperature: minimum temperature (integer), maximum temperature (integer), temperature step (float); initial weight: single value (integer); maximum age of individual in years (integer) | relative growth rates and  final weights: table, file format: csv | 
|[`multi_dim.py`](./growth_model/models/multi_dim.py)| a multi-dimensional transient model (updated setup from [Sokolova et al. (2021)](https://academic.oup.com/icesjms/article/78/4/1519/6207631). The model immitates monthly growth and calculates weight at a certain age (weight-at-age) using multidimensional ocean temperature data (space-, depth- and time-varying) | [`multi_dim.toml`](./config/multi_dim.toml) | temperature: multi-dimensional temperature dataset in netCDF format (minimum 10 years time series); temporal boundaries: first and last year in a dataset (integers); geographic boundaries: latitudes, longitudes, depths levels (lists); maximum age of individual in years (integer) | annual multi-dimensional datasets for: a, b, growth rates, weight-at-age; file format: netCDF | 


