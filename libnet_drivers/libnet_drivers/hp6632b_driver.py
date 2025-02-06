from libnet_wrapper import libnet_wrapper 
import struct
import matplotlib.pyplot as plt
import numpy as np
import time

class hp6632b_driver:
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
    def set_output_on(self):
        self.write("OUTPUT ON")
    def set_output_off(self):
        self.write("OUTPUT OFF")
    def set_ovp_voltage(self,volt):
        self.write("VOLTAGE:PROTECTION %.2f"%volt)
    def get_ovp_voltage(self):
        return float(self.query("VOLTAGE:PROTECTION?"))
    def set_output_voltage(self,volt):
        self.write("VOLTAGE %.3f"%volt)
    def set_output_current(self,current):
        self.write("CURRENT %.3f"%current)
    def meas_curr_voltage(self):
        return float(self.query("MEASURE:VOLTAGE?"))
    def meas_curr_current(self):
        return float(self.query("MEASURE:CURRENT?"))
if __name__ == "__main__":
    hp6632b = hp6632b_driver("10.2.0.9",6)
    hp6632b.get_idn_str()
    hp6632b.set_output_on()
    hp6632b.set_output_voltage(2.5)
    print(hp6632b.meas_curr_voltage())
