# Mekong
Depository contains two csv files and one python code.

"simulated_Q_SSC_2015-2100.csv" contain simulated discharge (Q) and suspended sediment concentration (SSC) data at Chiang Saen from 2015 to 2100. 
Data were obtained from WEP_L hydrological model with meterological input from five CMIP6 models: CESM2, INM-CM5, MPI_ESM1, NorESM2-MM and TaiESM1.

"simulated_Q_SSC_2015-2019.csv" contain simulated discharge (Q) and suspended sediment concentration (SSC) data at Chiang Saen from 2015 to 2019.
Data were obtained from WEP_L hydrological model with meterological input from real meteorological variables during 2015-2019.
Qsim(cms) and EQ(cms) are simulated discharge and its associated error.
Water released (Mm3/d) and EWater released (Mm3/d) are observed water released from Chinese cascade during 2015-2019 operations.
SSCsim (kt/Mm3) and ESSC(kt/Mm3) simulated suspended sediment concentration and its associated error.
Date year arbitarily set at 2021 for ease of coding

"sluicing_operation.py" documents how the following variables can be calculated:
1. Discharge released at Chiang Saen from sluicing operation
2. Sediment releasd at Chiang Saen from sluicing operation
3. Percentage of active storage of Chinese cascade can be filled
Code was built to run with "simulated_Q_SSC_2015-2100.csv" but can be modified accordingly

Please cite source if data was used in any way.
