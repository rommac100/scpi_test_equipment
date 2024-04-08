from libnet_wrapper import libnet_wrapper 
import struct
import matplotlib.pyplot as plt
import numpy as np
import time

class hp34401_driver:
    def __init__(self, host, addr):
        self.host = host
        self.addr = addr
        self.gpib_driver = libnet_wrapper.GPIBDriver(self.host,self.addr)
    def query(self,command_str,delay=.2):
        self.write(command_str)
        time.sleep(delay)
        return self.read()
    def read(self):
        return self.gpib_driver.read()
    def write(self,command_str):
        self.gpib_driver.write(command_str.encode("UTF-8"))
    def meas_dc_voltage(self):
        return float(self.query("MEASure:VOLTage:DC?"))
    def meas_dc_current(self):
        return float(self.query("MEASURE:CURRENT:DC?"))
    def get_configuration(self):
        return self.query("CONFIGURE?")
    def get_error_list(self):
        return self.query("SYSTEM:ERRor?")
    def get_measurement(self):
        return self.query("MEASURE?")
    def get_idn_str(self):
        idn_str = self.query("*IDN?")
        print(idn_str)
        return idn_str
    
if __name__ == "__main__":
    hp34401 = hp34401_driver("10.2.0.9",22)
    hp34401.get_idn_str()
    print(hp34401.get_error_list())
    print(hp34401.meas_dc_voltage())
