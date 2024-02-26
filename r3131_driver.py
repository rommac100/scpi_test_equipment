from libnet_wrapper import GPIBDriver 
import struct
import matplotlib.pyplot as plt
import numpy as np

class r3131_driver:
    def __init__(self, host, addr):
        self.host = host
        self.addr = addr
        self.gpib_driver = GPIBDriver(self.host,self.addr)
    def get_idn_str(self):
        idn_str = self.gpib_driver.query(b"*IDN?").decode()
        print(idn_str)
        return idn_str
    # returns int array
    def get_binary_trace_data(self):
        data_out = self.gpib_driver.read_binary_data(b'TBA?')
        data_int = struct.unpack_from(">"+"%dh"%(len(data_out)/2),data_out)
        return data_int
    def get_sweep_mode(self):
        return self.gpib_driver.query(('SWM?').encode('UTF-8')).decode()
    def set_sweep_mode_single(self):
        self.gpib_driver.write(b'SWM SI')
    def set_sweep_mode_cont(self):
        self.gpib_driver.write(b'SWM CONTS')
    def get_center_frequency(self):
        return self.gpib_driver.query(b'CF?').decode().rstrip()
    def get_span(self):
        return self.gpib_driver.query(b'SP?').decode().rstrip()
    def sweep(self):
        self.gpib_driver.write(b'TS')
    def plot_trace_a(self):
        self.set_sweep_mode_single()
        self.sweep()
        data_int = self.get_binary_trace_data()
        cf = int(float(self.get_center_frequency()))
        span = int(float(self.get_span()))
        freqs = np.linspace(cf-span/2,cf+span/2,num=len(data_int))
        plt.plot(freqs,data_int)

if __name__ == "__main__":
    r3131 = r3131_driver("10.2.0.9",8)
    r3131.get_idn_str()
    print(r3131.get_center_frequency())
    r3131.plot_trace_a()
    plt.savefig("test.png")
    #r3131.get_binary_trace_data()
