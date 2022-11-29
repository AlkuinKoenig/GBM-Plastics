# microplastics_boxmodel

27 Nov 2022 Jeroen Sonke & Alkuin Koenig (jeroen.sonke@get.omp.eu and Alkuin.Koenig@gmx.de)

- Please read the original paper (Sonke et al, 2023, Microplastics & Nanoplastics) to understand how the box model works.
- the "main script" is "boxmodel.py". This script will take a .json input file for the parameters (k values, etc) and will output a .csv file with the results. A standard .json input file is given, but new ones can be generated with the "boxmodel parameters.py" script. The purpose of this script is to calculate mass transfer coeffcients, k, (based on plastic mass, and fluxes from the literature), and write them to the .json file. If you make such changes, make sure to update the name of the .json file to import, in the "boxmodel.py" script.
- In "boxmodel.py" you can choose from four plastics release scenarios, 3 of which are discussed in Sonke et al., 2023 MNP:
1 'base', also BAU (business as usual) plastics production, waste generation and waste management (discard, incineration, recycling), basedon Geyer et al., 2017 SciAdv.
2 'SCS' (systems change scenario), simulating feasible best policy, with lower production, less mismanaged waste etc, based on Lau Winnie et al., 2020 Science.
3 'Full stop' in 2025, simulating P, LMP, SMP propagation through the model if we stop producing plastics and waste in 2025.
4 A 1y 'pulse' scenario, simulating also P, LMP, SMP propagation
One can also select one of three cleanup 'remediation' scenarios which are discussed in Sonke et al., 2023 MNP:
1 no cleanup
2 3% per year cleanup of the discarded P pool
3 3% per year cleanup of the discarded P, LMP, SMP pools
There is an option in "boxmodel.py" to also include the used parameters in the output as metadata.
- forcing functions for the four scenarios (plastics production, waste generation, waste management) are in "boxmodel_forcings.py". They should get automatically imported when you run "boxmodel.py". The forcing functions consiste of polynomial equations for the BAU, SCS etc scenarios that were fitted to the original data fom the associated papers. The original forcing data (plastics production, waste generation, waste management) can be found in the SI of Sonke et al., 2023.
- The output of "boxmodel.py" will be saved automatically as .csv in your working folder. Output file names will be generated automatically and will depend on your system time when the script was run, as well as the input file that has been used.
- an example script to plot output is included. You need to feed this script a "model output .csv" file, as created by "boxmodel.py".

