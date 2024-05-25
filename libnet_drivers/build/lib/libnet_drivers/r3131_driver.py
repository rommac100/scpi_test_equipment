from libnet_wrapper import libnet_wrapper
import struct
import matplotlib.pyplot as plt
import numpy as np
import time

class r3131_driver:
    def __init__(self, host, addr):
        self.host = host
        self.addr = addr
        self.gpib_driver = libnet_wrapper.GPIBDriver(self.host,self.addr)
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
    def read_binary_data(self,command):
        self.write(s)
        data = self.read()
        data_out = bytearray()
        while (len(data) > 0):
            data_out.extend(data)
            data = self.read()

        return data_out
    # returns int array
    def get_ascii_trace_data(self):
        self.write("TAA?")
        data_list = []
        data = self.read()
        while (len(data_list) < 501):
            data_list.append(data)
            data = self.read()
        return data
    def get_binary_trace_data(self):
        data_out = self.read_binary_data('TBA?')
        #data_int = struct.unpack_from(">"+"%dh"%(len(data_out)/2),data_out)
        return data_out
    def get_sweep_mode(self):
        return self.query('SWM?')
    def set_sweep_mode_single(self):
        self.write('SWM SI')
    def set_sweep_mode_cont(self):
        self.write('SWM CONTS')
    def get_center_frequency(self):
        return self.query('CF?').rstrip()
    def get_span(self):
        return self.query('SP?').rstrip()
    def sweep(self):
        self.write('TS')
    def get_sweep_time(self):
        return float(self.query('ST?').rstrip())
    def turn_on_marker(self,marker_number):
        self.gpib_driver.write(("MN%d"%marker_number).encode("UTF-8"))
    def marker_pk_search(self):
        self.gpib_driver.write(b'MKPK')
    def get_marker_frequency(self):
        return float(self.query('MF?').rstrip())
    def get_marker_level(self):
        return float(self.query('ML?').rstrip())
    def wait_for_opc(self):
        op_status_reg = self.query('*ESR?')
        print(op_status_reg)
        if (op_status_reg & 0x8):
            print("CURRENTLY SWEEPING")
    def plot_trace_a(self,filename_csv="",filename_image="",show_plot=0):
        self.set_sweep_mode_single()
        sweep_time = self.get_sweep_time()
        print("sweep time: %f"%sweep_time)
        self.sweep()
        time.sleep(20)
        data_int = self.get_binary_trace_data()
        cf = int(float(self.get_center_frequency()))
        span = int(float(self.get_span()))
        freqs = np.linspace(cf-span/2,cf+span/2,num=len(data_int))
        plt.plot(freqs,data_int)
        if (show_plot==1):
            plt.show()

        if (filename_csv != ""):
            combined_array = np.zeros((len(freqs),2))
            combined_array[:,0]=freqs
            combined_array[:,1]=data_int
            np.savetxt(filename_csv,combined_array,fmt="%.5f",delimiter=',',header='Frequency (Hz), Magnitude (dBm)',comments='')
        
        if (filename_image != ""):
            plt.savefig(filename_image)

if __name__ == "__main__":
    r3131 = r3131_driver("10.2.0.9",8)
    r3131.get_idn_str()
    #print(r3131.get_center_frequency())
    #data = r3131.get_binary_trace_data()
    #print(r3131.gpib_driver.query(b'ST?'))
    #r3131.turn_on_marker(1)
    #r3131.marker_pk_search()
    #print(r3131.get_marker_frequency())
    #print(r3131.get_marker_level())
    #r3131.plot_trace_a(filename_image="test.png",filename_csv="test.csv")
