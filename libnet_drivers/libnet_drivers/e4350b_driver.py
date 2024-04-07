from libnet_wrapper import libnet_wrapper 
import struct
import matplotlib.pyplot as plt
import numpy as np
import time

class e4350b_driver:
    def __init__(self, host, addr):
        self.host = host
        self.addr = addr
        self.gpib_driver = libnet_wrapper.GPIBDriver(self.host,self.addr)
    def query(self,command_str):
        return self.gpib_driver.query(command_str.encode("UTF-8"))
    def read(self):
        return self.gpib_driver.read()
    def write(self,command_str):
        self.gpib_driver.write(command_str.encode("UTF-8"))
    def get_idn_str(self):
        idn_str = self.query("*IDN?")
        print(idn_str)
        return idn_str
    # Setting outputs
    def set_output_on(self):
        self.write("OUTP ON")
    def set_output_off(self):
        self.write("OUTP OFF")
    def get_output_state(self):
        return self.query("OUTPUT:STATE?")
    def set_output_voltage(self,volt):
        self.write("VOLT:LEV:IMM %.2f"%volt)
    def set_output_current(self,current):
        self.write("CURR:LEV:IMM %.2f"%current)
    # Measurement Functions
    def meas_curr_voltage(self):
        return self.query("MEASURE:VOLTAGE?")
    def meas_curr_current(self):
        return self.query("MEASURE:CURRENT?")
    # Current Mode Settings
    def set_current_mode_fixed(self):
        self.write("SOURCE:CURRENT:MODE FIXED")
    def set_current_mode_simulator(self):
        self.write("SOURCE:CURRENT:MODE SAS")
    def get_output_voltage(self):
        return self.query("SOURCE:VOLT?")
    def get_current_mode(self):
        return self.query("SOURCE:CURRENT:MODE?")
    
if __name__ == "__main__":
    e4350b = e4350b_driver("10.2.0.9",7)
    e4350b.get_idn_str()
    e4350b.set_current_mode_simulator()
    print(e4350b.get_current_mode())
    e4350b.set_current_mode_fixed()
    print(e4350b.get_current_mode())
