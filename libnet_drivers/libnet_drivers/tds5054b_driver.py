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
        #return data_out
    def read_waveform_data(self):
        print('reading waveform data')
        self.write("DATA:SOURCE CH1")
        self.write("DATA:ENCDG ASCII")
        print(self.query('DATA:STOP?'))
        print(self.query('DATA:START?'))
        print(self.query("DATA?"))

        print(self.query("CURVE?"))
        data_list = []
        data = self.read()
        while (len(data_list) < 5001):
            print(data)
            data_list.append(data)
            data = self.read()


    def set_measurement_pk_pk(self,channel):
        print('reading measurement data')

    def set_measurement_mean(self,channel):
        print('reading measurement data')


    def read_measurement_data(self):
        print('reading measurement data')
    def transfer_hard_copy(self,filename):
        self.write('*CLS')
        self.write('FILESYSTEM:CWD "C:\\TekScope\\images"')
        self.write('HARDCOPY:PORT FILE')
        self.write('HARDCOPY:FILENAME "C:\\TekScope\\images\\TekH001.PNG"')
        self.write('HARDCOPY START')
        self.query('*OPC?')
        time.sleep(3)
        self.write('FILESYSTEM:PRINT "C:\\TekScope\\images\\TekH001.PNG",GPIB')
        for ii in range(50):
            print(self.read())


    # returns int array
if __name__ == "__main__":
    tds5054b = tds5054b_driver("10.2.0.9",26)
    tds5054b.get_idn_str()    
    tds5054b.read_waveform_data()
    #tds5054b.transfer_hard_copy("test")
