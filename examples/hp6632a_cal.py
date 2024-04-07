#!/usr/bin/python3.5

# This calibration program is written according to the HP6632A /
# HP6633A / HP6634A calibration manual, Appendix A.
#
# The HP-34401A is used as the measuring device; other meters can also
# be used with little (?) adaptation.
#
# The resolution of the PSU integrate meter is limited (12 bits or
# 4096 steps), so it's unlikely that you will get a perfect
# readout. For example, the HP6632A has a maximum voltage of 20V,
# which gives a resolution of 20.0 / 4096 or around 5mV at best.
#
# You will likely have to change the devices GPIB addresses below.
#
# Version: 1.0 (2021-01-14)
#
# (c) 2021 Damien Douxchamps


# Modified for ENET Support

# TODO:
#
# - Current calibration. I don't have a megaspec 0.1 Ohm resistor to
#   test this. The procedure is included but deactivated since it's
#   untested.

import time
from libnet_drivers import hp34401_driver
from libnet_drivers import hp6632_driver

psu_address = 6 # the GPIB address of your PSU
dvm_address = 22 # the GPIB address of your multimeter (HP34401A)
ip_address = "10.2.0.9"
measurement_pause = 0.2 # in seconds. Does not need to be changed.

# 100mOhm (0.05%) is the value of the recommended shunt for current
# measurements. These beasts are _expensive_.
Shunt_r = 0.1 # 100mOhm
# Connect to our instrumentsQ

psu = hp6632_driver.hp6632_driver(ip_address,psu_address)
dvm = hp34401_driver.hp34401_driver(ip_address,dvm_address)
print("Device list:")
psu_model=psu.query("ID?").rstrip()
print("PSU: " + psu_model)
print("DVM: " + str(dvm.query("*IDN?").rstrip()))

# PSU specific data, see manual page A-5, line 490-510

if psu_model == "HP6632A":
    G_vprog = 268369.9
    G_vrb = 65.536
    G_iprog = 26836.99
    G_irb = 6.5536
    FS_V = 20
    FS_I = 5
    MIN_I = 0.02
elif psu_model == "HP6633A":
    G_vprog = 268369.9
    G_vrb = 65.536
    G_iprog = 26836.99
    G_irb = 6.5536
    FS_V = 50
    FS_I = 2
    MIN_I = 0.008
elif psu_model == "HP6634A":
    G_vprog = 2683699
    G_vrb = 655.36
    G_iprog = 26836.99
    G_irb = 6.5536
    FS_V = 100
    FS_I = 1
    MIN_I = 0.004
else:
    print("Unrecognized power supply '" + psu_model + "', aborting")
    quit()

print("=========================================")
print("===== VOLTAGE CALIBRATION PROCEDURE =====")
print("=========================================")

psu.write("CMODE 1") # enter calibration mode

psu.write("OUT 1") # output ON

psu.write("OVSET 255;ISET 4095")
psu.write("VSET 4095")
time.sleep(measurement_pause)

Vrb_hi = float(psu.query("VOUT?"))
print("HP-6632A : Vrb_hi  = %d" % (Vrb_hi))

Vout_hi=float(dvm.query("MEASURE:VOLTAGE:DC?"))
print("HP-34401A: Vout_hi = %f" % (Vout_hi))

psu.write("VSET 0")
time.sleep(measurement_pause)

Vrb_lo = float(psu.query("VOUT?"))
print("HP-6632A : Vrb_lo  = %d" % (Vrb_lo))

Vout_lo=float(dvm.query("MEASURE:VOLTAGE:DC?"))
print("HP-34401A: Vout_lo = %f" % (Vout_lo))

K_vprog = G_vprog/(Vout_hi-Vout_lo)
K_vrb   = G_vrb*(Vrb_hi-Vrb_lo)/(Vout_hi-Vout_lo)
O_vprog = -Vout_lo
O_vrb   = (Vout_hi-Vout_lo)*Vrb_lo/(Vrb_hi-Vrb_lo)-Vout_lo
print("K_vprog = " + str(K_vprog))
print("K_vrb   = " + str(K_vrb))
print("O_vprog = " + str(O_vprog))
print("O_vrb   = " + str(O_vrb))

# Save parameters in _volatile_ RAM
psu.write("CDATA 1,%.6f,%.6f" % (K_vprog, O_vprog))
psu.write("CDATA 2,%.6f,%.6f" % (K_vrb, O_vrb))

psu.write("CMODE 0") # leave calibration mode

# Voltage calibration verification procedure

psu.write("ISET " + str(FS_I))
psu.write("VSET 0")
time.sleep(measurement_pause)

Vout_lo=float(dvm.query("MEASURE:VOLTAGE:DC?"))
Vrb_lo = float(psu.query("VOUT?"))
print("Measured: Vout_lo = %6.3f V, error = %6.3f mV" % (Vout_lo, Vout_lo*1000))
print("Readback: Vrb_lo  = %6.3f V, error = %6.3f mV" % (Vrb_lo, Vrb_lo*1000))

psu.write("VSET " + str(FS_V))
time.sleep(measurement_pause)

Vout_hi=float(dvm.query("MEASURE:VOLTAGE:DC?"))
Vrb_hi = float(psu.query("VOUT?"))
print("Measured: Vout_hi = %6.3f V, error = %6.3f mV" % (Vout_hi, (Vout_hi-FS_V)*1000))
print("Readback: Vrb_lo  = %6.3f V, error = %6.3f mV" % (Vrb_hi, (Vrb_hi-FS_V)*1000))

print("\n*** Voltage calibration finished. ***") 
print("Check the measured and readback voltages above against the PSU specs.")
print("If the results are within specifications type \"Save\" (case sensitive).")

an=input("Otherwise type <enter> and switch your PSU OFF to keep the old calibration constants.\n > ")
if an == "Save":
    print("Saving the calibration parameters...")
    psu.write("CSAVE") # save constants in _non_volatile_ EEPROM
    print("Done.")
else:
    print("Calibration parameters were *** NOT *** saved.")

# The current calibration is NOT tested and thus skipped.

if False:

    print("=========================================")
    print("===== CURRENT CALIBRATION PROCEDURE =====")
    print("=========================================")

    psu.write("CMODE 1")

    psu.write("OUT 1")

    psu.write("VSET 4095")
    psu.write("ISET 4095")
    time.sleep(measurement_pause)

    Irb_hi = float(psu.query("IOUT?"))
    print("HP-6632A : Irb_hi  = %d" % (Irb_hi))

    Iout_hi=float(dvm.query("MEASURE:VOLTAGE:DC?"))
    Iout_hi=Iout_hi/Shunt_r
    print("HP-34401A: Iout_hi = %f" % (Iout_hi))

    psu.write("ISET 0")
    time.sleep(measurement_pause)

    Irb_lo = float(psu.query("IOUT?"))
    print("HP-6632A : Irb_lo  = %d" % (Irb_lo))

    Iout_lo=float(dvm.query("MEASURE:VOLTAGE:DC?"))
    Iout_lo=Iout_lo/Shunt_r
    print("HP-34401A: Iout_lo = %f" % (Iout_lo))

    psu.write("ISET 50")
    time.sleep(measurement_pause)

    Irb_50 = float(psu.query("IOUT?"))
    print("HP-6632A : Irb_50  = %d" % (Irb_50))

    Iout_50=float(dvm.query("MEASURE:VOLTAGE:DC?"))
    Iout_50=Iout_50/Shunt_r
    print("HP-34401A: Iout_50 = %f" % (Iout_50))

    K_iprog = G_iprog/(Iout_hi-Iout_lo)
    K_irb   = G_irb*(Irb_hi-Irb_50)/(Iout_hi-Iout_50)
    O_iprog = -Iout_lo
    O_irb   = (Iout_hi-Iout_50)*Irb_50/(Irb_hi-Irb_50)-Iout_50
    print("K_iprog = " + str(K_iprog))
    print("K_irb   = " + str(K_irb))
    print("O_iprog = " + str(O_iprog))
    print("O_irb   = " + str(O_irb))

    psu.write("CDATA 3,%.6f,%.6f" % (K_iprog, O_iprog))
    psu.write("CDATA 4,%.6f,%.6f" % (K_irb, O_irb))

    psu.write("CMODE 0")

    # Current calibration verification procedure

    psu.write("VSET " + str(FS_V))
    psu.write("ISET 0")
    time.sleep(measurement_pause)

    Iout_lo_check=float(dvm.query("MEASURE:VOLTAGE:DC?"))
    Iout_lo_check=Iout_lo_check/Shunt_r
    print("HP-34401A: Iout_lo = %6.3f A, error = %6.3f mA" % (Iout_lo_check, Iout_lo_check*1000))

    psu.write("ISET " + str(FS_I))
    time.sleep(measurement_pause)
    
    Iout_hi_check=float(dvm.query("MEASURE:VOLTAGE:DC?"))
    Iout_hi_check=Iout_hi_check/Shunt_r
    print("HP-34401A: Vout_hi = %6.3f A, error = %6.3f mA" % (Iout_hi_check, (Iout_hi_check-FS_I)*1000))

    psu_write("OUT 0")

    # calibration parameters can be saved here, see voltage section.
    
