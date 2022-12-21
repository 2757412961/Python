import PyCO2SYS as pyco2
from PyCO2SYS import CO2SYS
import math

par1type = 1  # The first parameter supplied is of type "1", which means "alkalinity"
par1 = 2680  # value of the first parameter
par2type = 3  # The second parameter supplied is of type "3", which means "pH"
par2 = 8.2  # value of the second parameter
sal = 35  # Salinity of the sample
tempin = 25  # Temperature at input conditions
tempout = 25  # Temperature at output conditions
presin = 0  # Pressure    at input conditions
presout = 0  # Pressure    at output conditions
sil = 50  # Concentration of silicate  in the sample (in umol/kg)
po4 = 2  # Concentration of phosphate in the sample (in umol/kg)
pHscale = 3  # pH scale at which the input pH is reported ("1" means "Total Scale") ("3" means Free Scale)
k1k2c = 4  # Choice of H2CO3 and HCO3- dissociation constants K1 and K2 ("4" means "Mehrbach refit")
kso4c = 1  # Choice of HSO4- dissociation constants KSO4 ("1" means "Dickson")

# From 6.5 DKH to 14 DKH
dkh_tests = [
    "2340",
    "2376",
    "2412",
    "2448",
    "2484",
    "2520",
    "2556",
    "2592",
    "2628",
    "2664",
    "2700",
    "2736",
    "2772",
    "2808",
    "2844",
    "2880",
    "2916",
    "2952",
    "2988",
    "3024",
    "3060",
    "3096",
    "3132",
    "3168",
    "3204",
    "3240",
    "3276",
    "3312",
    "3348",
    "3384",
    "3420",
    "3456",
    "3492",
    "3528",
    "3564",
    "3600",
    "3636",
    "3672",
    "3708",
    "3744",
    "3780",
    "3816",
    "3852",
    "3888",
    "3924",
    "3960",
    "3996",
    "4032",
    "4068",
    "4104",
    "4140",
    "4176",
    "4212",
    "4248",
    "4284",
    "4320",
    "4356",
    "4392",
    "4428",
    "4464",
    "4500",
    "4536",
    "4572",
    "4608",
    "4644",
    "4680",
    "4716",
    "4752",
    "4788",
    "4824",
    "4860",
    "4896",
    "4932",
    "4968",
    "5004",
    "5040"
]

ph_tests = [
    "7.0",
    "7.1",
    "7.2",
    "7.3",
    "7.4",
    "7.5",
    "7.6",
    "7.7",
    "7.8",
    "7.9",
    "8.0",
    "8.1",
    "8.2",
    "8.3",
    "8.4",
    "8.5",
    "8.6",
    "8.7",
    "8.8",
    "8.9",
    "9.0"
]

print("DKH/PH", end=",")
print(','.join(str(x) for x in ph_tests))


def truncate(f, n):
    return math.floor(f * 10 ** n) / 10 ** n


if __name__ == '__main__':
    print(pyco2.sys(par1=1.3, par1_type=1, par2=100, par2_type=4))

    for dkh_value in dkh_tests:
        print("")
        dkh = float(dkh_value) / 1000 / 0.36
        print(truncate(dkh, 1), end=",")
        for ph_value in ph_tests:
            par1 = dkh_value
            par2 = ph_value
            # Do the calculation. See CO2SYS's help for syntax and output format
            CO2dict = CO2SYS(
                par1,
                par2,
                par1type,
                par2type,
                sal,
                tempin,
                tempout,
                presin,
                presout,
                sil,
                po4,
                pHscale,
                k1k2c,
                kso4c,
            )

            # dkh = CO2dict["TAlk"][0]/1000*2.8
            # print(dkh)
            print(CO2dict["pHoutTOTAL"][0])
            print("%.0f" % CO2dict["xCO2out"][0], end=",")
