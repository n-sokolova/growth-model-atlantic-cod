<!--
SPDX-FileCopyrightText: 2021 Alfred Wegener Institute Helmholtz Centre for Polar and Marine Research (AWI)
SPDX-License-Identifier: CC-BY-4.0
-->

# Description of Atlantic cod growth model

Atlantic cod growth model is a physiology-related growth model that simulates size- and temperature-dependent growth of Atlantic cod *(Gadus morhua)*. The growth model relates temperature and growth rates based on the absolute reaction rate theory with growth inhibition at higher temperatures, including Arrhenius equation of temperature-dependent chemical reaction rates (Clarke, 2017). The model was calibrated with the results from growth experiments for Iceland cod ([Björnsson and Steinarsson, 2002](https://cdnsciencepub.com/doi/10.1139/f02-028); [Björnsson et al., 2007](https://www.sciencedirect.com/science/article/pii/S0044848607005182)). The growth experiments cover the temperature range 2–16 °C (T = 2, 4, 7, 8, 10, 12, 13, 16 °C), and the body weight range 0.001–8 kg. Mathematical description, details on calibration, and procedure of model development are described in the study of [Butzin and Pörtner (2016)](https://onlinelibrary.wiley.com/doi/10.1111/gcb.13375). 

Core model assumptions:
- the growth model assumes that the rate at which an organism grows, depends on the value of its own body mass, i.e. allometric growth ([White and Kearney, 2014](https://pubmed.ncbi.nlm.nih.gov/24692144/));
- it considers immediate organismic response to changes in temperatures ([Butzin and Pörtner, 2016](https://onlinelibrary.wiley.com/doi/10.1111/gcb.13375));
- the model disregards larval growth variations, vertical, or horizontal movements and does not expect ontogenetic habitat shifts;
- the model expects unlimited food availability and a homogeneous thermal environment during growth (based on data from [Björnsson and Steinarsson, 2002](https://cdnsciencepub.com/doi/10.1139/f02-028); [Björnsson et al., 2007](https://www.sciencedirect.com/science/article/pii/S0044848607005182)). 


# References

- Björnsson, B., and Steinarsson, A. 2002. The food-unlimited growth rate of Atlantic cod (Gadus morhua). Canadian Journal of Fisheries and Aquatic Sciences, 59: 494–502.


- Björnsson, B., Steinarsson, A., and Árnason, T. 2007. Growth model for Atlantic cod (Gadus morhua): Effects of temperature and body weight on growth rate. Aquaculture, 271: 216–226.


- Butzin, M., and Pörtner, H.-O. 2016. Thermal growth potential of Atlantic cod by the end of the 21st century. Global Change Biology, 22: 4162–4168.


- Clarke, A. (2017). Principles of Thermal Ecology: Temperature, Energy, and Life. Oxford University Press. https://doi.org/10.1093/oso/9780199551668.001.0001


- White, C. R., and Kearney, M. R. 2014. Metabolic Scaling in Animals: Methods, Empirical Results, and Theoretical Explanations. In Comprehensive Physiology, pp. 231–256. 
