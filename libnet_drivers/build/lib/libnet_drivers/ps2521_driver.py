from libnet_wrapper import libnet_wrapper
import struct
import matplotlib.pyplot as plt
import numpy as np

class ps2521_driver:
    def __init__(self, host, addr):
        self.host = host
        self.addr = addr
        self.gpib_driver = libnet_wrapper.GPIBDriver(self.host,self.addr)
    def query(self,command_str):
        return self.gpib_driver.query(command_str.encode("UTF-8")).decode()
    def read(self):
        return self.gpib_driver.read().decode()
    def write(self,command_str):
        self.gpib_driver.write(command_str.encode("UTF-8"))
    def get_idn_str(self):
        idn_str = self.query("*IDN?")
        print(idn_str)
        return idn_str
    def select_output(self,output_number):
        self.write("INSTRUMENT:NSELECT %d"%output_number)
    def get_selected_output(self):
        return self.query("INSTR:NSEL?")
    def set_output_on(self):
        self.write("OUTPUT:STATE 1")
    def set_output_off(self):
        self.write("OUTPUT:STATE 0")
    def get_output_state(self):
        return self.query("OUTPUT:STATE?")
    def set_output_voltage(self,volt):
        self.write("SOURCE:VOLTAGE %.2f"%volt)
    def set_output_current(self,curr):
        self.write("SOURCE:CURRENT %.3f"%curr)
    def get_output_voltage(self):
        return self.query("SOURCE:VOLT?")
    def get_output_current(self):
        return self.query("SOURCE:CURRENT?")
    def meas_curr_voltage(self):
        return self.query("MEASURE:VOLTAGE?")
    def meas_curr_current(self):
        return self.query("MEASURE:CURRENT?")
if __name__ == "__main__":
    ps2521 = ps2521_driver("10.2.0.9",6)
    ps2521.get_idn_str()
    ps2521.select_output(1)
    ps2521.set_output_voltage(6)
    ps2521.set_output_current(.3)
    print(ps2521.get_output_current())
    print(ps2521.get_output_voltage())
    ps2521.set_output_on()
    print(ps2521.meas_curr_voltage())
    print(ps2521.meas_curr_current())
