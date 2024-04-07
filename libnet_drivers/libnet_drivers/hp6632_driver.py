from libnet_wrapper import libnet_wrapper 
import struct
import matplotlib.pyplot as plt
import numpy as np
import time

class hp6632_driver:
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
        idn_str = self.query("ID?")
        print(idn_str)
        return idn_str
    def set_output_on(self):
        self.write("OUT 1")
    def set_output_off(self):
        self.write("OUT 0")
    def set_output_voltage(self,volt):
        self.write("VSET %.2f"%volt)
    def set_output_current(self,current):
        self.write("ISET %.2f"%current)
    def meas_curr_voltage(self):
        return self.query("VOUT?")
    def meas_curr_current(self):
        return self.query("IOUT?")
if __name__ == "__main__":
    hp6632 = hp6632_driver("10.2.0.9",6)
    hp6632.get_idn_str()
    hp6632.set_output_on()
    hp6632.set_output_voltage(2.5)
    print(hp6632.meas_curr_voltage())
