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
    # returns int array
    def get_binary_trace_data(self):
        data_out = self.gpib_driver.read_binary_data(b'TBA?')
        data_int = struct.unpack_from(">"+"%dh"%(len(data_out)/2),data_out)
        return data_int
    def get_sweep_mode(self):
        return self.gpib_driver.query(('SWM?').encode('UTF-8'))
    def set_sweep_mode_single(self):
        self.gpib_driver.write(b'SWM SI')
    def set_sweep_mode_cont(self):
        self.gpib_driver.write(b'SWM CONTS')
    def get_center_frequency(self):
        return self.gpib_driver.query(b'CF?').rstrip()
    def get_span(self):
        return self.gpib_driver.query(b'SP?').rstrip()
    def sweep(self):
        self.gpib_driver.write(b'TS')
    def get_sweep_time(self):
        return float(self.gpib_driver.query(b'ST?').rstrip())
    def turn_on_marker(self,marker_number):
        self.gpib_driver.write(("MN%d"%marker_number).encode("UTF-8"))
    def marker_pk_search(self):
        self.gpib_driver.write(b'MKPK')
    def get_marker_frequency(self):
        return float(self.gpib_driver.query(b'MF?').rstrip())
    def get_marker_level(self):
        return float(self.gpib_driver.query(b'ML?').rstrip())
    def wait_for_opc(self):
        op_status_reg = self.gpib_driver.query(b'*ESR?')
        print(op_status_reg)
        if (op_status_reg & 0x8):
            print("CURRENTLY SWEEPING")
    def plot_trace_a(self,filename_csv="",filename_image=""):
        self.set_sweep_mode_single()
        sweep_time = self.get_sweep_time()
        self.sweep()
        time.sleep(sweep_time+.5)
        data_int = self.get_binary_trace_data()
        cf = int(float(self.get_center_frequency()))
        span = int(float(self.get_span()))
        freqs = np.linspace(cf-span/2,cf+span/2,num=len(data_int))
        plt.plot(freqs,data_int)
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
