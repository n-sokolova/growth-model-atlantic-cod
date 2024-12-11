<!--
SPDX-FileCopyrightText: 2022 Alfred-Wegener-Institut, Helmholtz-Zentrum für Polar- und Meeresforschung (AWI)
SPDX-License-Identifier: MIT
-->


<br />
<h1 align="center">Growth Model Atlantic Cod</h1>

<p align="center">

The Atlantic cod growth model is a single-species bio-physical growth model that simulates temperature- and size-dependent growth of Atlantic cod *Gadus morhua*.

</p>
</div>


<!--===============-->
<!--=== Chapter ===-->
<!--===============-->
# About the project

The model is derived from the experimental data of [Björnsson and Steinarsson (2002)][bjoernsson_2002], [Björnsson et al. (2007)][bjoernsson_2007]. It was initially published by [Butzin and Pörtner (2016)][butzin_2016] and extended to a multi-dimensional version by [Sokolova et al. (2021)][sokolova_2021]. The model simulates daily growth of cod observed in laboratory experiments, as well as monthly growth under "real-world" open sea conditions. As an input the growth model uses temperature data of different dimensions. The outputs of the growth model are growth rate and individual weight. Growth model biological and physiological assumptions are described in [growth-model-description](./docs/growth_model_description.md).

The following [web-page][cod-website] provides conceptual details and displays growth model outputs in an interactive format.

<!--===============-->
<!--=== Chapter ===-->
<!--===============-->
# Getting started

## Prerequisites

* To work with the package you need to have at least Python 3.9 installed.
* The package can be installed in any desired Python virtual environment.

## Installation

The project can simply be installed from the repository into the desired Python
virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
pip install git+https://github.com/n-sokolova/growth-model-atlantic-cod.git
```

After installing the project as described, the `cod-growth-model` command is
available.

<!--===============-->
<!--=== Chapter ===-->
<!--===============-->

## Usage of the `cod-growth-model`

**Syntax**

```bash
cod-growth-model [CONFIG FILE] [OUTPUT FILE or FOLDER]
```

For more help type:

```bash
cod-growth-model --help
```

**Step 1. Choose the model version and adapt the corresponding configuration file.**

- Choose the model from the list: [the model file](./docs/growth_models.md)
- Adapt the corresponding config file `*.toml`: [config file](./config/): define
  input parameters (e.g. initial weight, temperature)

**Step 2. Run the installed growth model with the desired output path.**

### Examples

The following examples assume that the toml files are available on the file
system. This can be achieved by cloning the repository as follows:

```bash
git clone git@codebase.helmholtz.cloud:awi_paleodyn/growth-model-atlantic-cod.git
```

**base model**

*base* model run requires config file, output folder and file name (the same for *one_init_weight*, *one_imput_temp*, *one_dim* models):

```bash
cod-growth-model ./config/base.toml ./output/base_model.csv
```

*base* model output:

```log
Initial weight:  1000 g
Input temperature:  10 °C
Relative growth rate:  0.0046543 g per day
Calculated weight:  1004.65432 g
```

**multi_dim model**

*multi_dim* model run requires a configuration file and an output folder:

```bash
cod-growth-model ./config/multi_dim.toml ./output/
```

*multi_dim* model automatically gives the file names. The .netcdf files are
saved in the specified output directory.

<!--===============-->
<!--=== Chapter ===-->
<!--===============-->

# License

Please see the file [LICENSE.md](https://gitlab.hzdr.de/awi_paleodyn/growth-model-atlantic-cod/-/blob/master/LICENSE.md) for further information about how the content is licensed.

<!--===============-->
<!--=== Chapter ===-->
<!--===============-->
# Citation

If you use this work in a research publication, please cite the specific version
that you used with [the citation metadata on Zenodo][zenodo].

You can find an overview about the different versions in the `changelog.md`.

<!--===============-->
<!--=== Chapter ===-->
<!--===============-->
# Contributors

- [Nadezhda Sokolova](https://www.linkedin.com/in/nadezhda-sokolova-phd-a6159b26a/) - main contact person
- Anja Rohner
- Thomas Förster
- Benjamin Wolff
- [Paul Gierz](https://github.com/pgierz)
- [Benjamin Thomas Schwertfeger](https://github.com/btschwertfeger)
- Markus Tobias Ruhland
- [Martin Butzin](https://www.marum.de/Dr.-martin-butzin.html)

## We welcome your contribution!

The repository is still under development and any feedback, suggestions,
technical contributions are highly welcome.

General Options:

- open an issue, if you have improvement ideas
- fork the project and contribute via merge request against the main branch of
  this repository

# Notes

- To keep submodule updated use the [instructions](https://devconnected.com/how-to-add-and-update-git-submodules/)

# References
- Björnsson, B., and Steinarsson, A. 2002. The food-unlimited growth rate of Atlantic cod (Gadus morhua). Canadian Journal of Fisheries and Aquatic Sciences, 59: 494–502. <p></p>


- Björnsson, B., Steinarsson, A., and Árnason, T. 2007. Growth model for Atlantic cod (Gadus morhua): Effects of temperature and body weight on growth rate. Aquaculture, 271: 216–226. <p></p>


- Butzin, M., and Pörtner, H.-O. 2016. Thermal growth potential of Atlantic cod by the end of the 21st century. Global Change Biology, 22: 4162–4168. https://doi.org/10.1111/gcb.13375  <p></p>


- Sokolova, N., Butzin, M., Dahlke, F., Werner, K.-M., Balting, D., Lohmann, G., Pörtner, H.-O. 2021. Exploring the role of temperature in observed inter-population differences of Atlantic cod (Gadus morhua) growth with a 4-dimensional modelling approach, ICES Journal of Marine Science, Volume 78, Issue 4, August 2021, Pages 1519–1529, https://doi.org/10.1093/icesjms/fsab043


<!---- Literature ---->
[bjoernsson_2002]: https://cdnsciencepub.com/doi/10.1139/f02-028
[bjoernsson_2007]: https://www.sciencedirect.com/science/article/pii/S0044848607005182
[butzin_2016]: https://onlinelibrary.wiley.com/doi/10.1111/gcb.13375
[sokolova_2021]: https://academic.oup.com/icesjms/article/78/4/1519/6207631?login=true

<!---- Links ---->
[zenodo]: https://doi.org/10.5281/zenodo.6705792
[download-wheel]: https://codebase.helmholtz.cloud/api/v4/projects/4188/jobs/artifacts/master/raw/dist/growth_model-1.0.1-py3-none-any.whl?job=build_wheel_package
[cod-website]: https://btschwertfeger.github.io/Growth-Model-Website/
[pip-autoremove]: https://github.com/invl/pip-autoremove
[growth-model-description]: https://gitlab.hzdr.de/awi_paleodyn/growth-model-atlantic-cod/-/blob/master/growth_model_description.md


