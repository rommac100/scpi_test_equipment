from libnet_wrapper import libnet_wrapper
import struct
import matplotlib.pyplot as plt
import numpy as np
import time

class tds5054b_driver:
    def __init__(self, host, addr):
        self.host = host
        self.addr = addr
        self.gpib_driver = libnet_wrapper.GPIBDriver(self.host,self.addr)
        self.max_data_value = 3392
        self.min_data_value = 512
    def get_idn_str(self):
        idn_str = self.gpib_driver.query(b"*IDN?")
        print(idn_str)
        return idn_str
    def query(self,command_str):
        return self.gpib_driver.query(command_str.encode("UTF-8"))
    def read(self):
        return self.gpib_driver.read()
    def write(self,command_str):
        self.gpib_driver.write(command_str.encode("UTF-8"))
    def read_binary_data(self,length):
        data = self.read()
        data_out = []
        print('test')
        while (len(data) < data_out):
           data_out.append(data)
           data = self.read()

        return data_out
    def transfer_hard_copy(self,filename):
        self.write('HARDCOPY:PORT FILE')
        self.write('HARDCOPY:FILENAME "C:\TekScope\images\TekH001.PNG"')
        self.write('HARDCOPY START')
        self.query('*OPC?')
        time.sleep(3)
        self.write('FILESYSTEM:READFILE "C:\TekScope\images\TekH001.PNG"')
        data = self.read_binary_data(640*480)
        print(data)


    # returns int array
if __name__ == "__main__":
    tds5054b = tds5054b_driver("10.2.0.9",26)
    tds5054b.write("*CLS")
    print(tds5054b.query("HARDCOPY?"))
    #tds5054b.get_idn_str()
    tds5054b.transfer_hard_copy("test")
