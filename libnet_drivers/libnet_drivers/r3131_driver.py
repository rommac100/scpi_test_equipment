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
    def read_binary_data(self,command_str):
        data_out = self.gpib_driver.read_binary_data(command_str.encode("UTF-8"))
        return data_out
    # returns int array
    def get_ascii_trace_data(self):
        self.write("TAA?")
        data_list = []
        data = self.read()
        while (len(data_list) < 501):
            #print(data)
            data_list.append(int(data))
            data = self.read()
        return data_list
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
        self.write(("MN%d"%marker_number))
    def marker_pk_search(self):
        self.write('MKPK')
    def get_marker_frequency(self):
        return float(self.query('MF?').rstrip())
    def get_marker_level(self):
        return float(self.query('ML?').rstrip())
    def get_ref_level(self):
        return float(self.query('RL?').rstrip())
    def set_marker_to_cf(self):
        self.set_marker_to_freq(float(self.get_center_frequency()))
    def set_marker_to_freq(self,freq):
        self.write("MN %d"%freq)
    def get_start_freq(self):
        return float(self.query('FA?').rstrip())
    def get_stop_freq(self):
        return float(self.query('FB?').rstrip())
    def set_start_freq(self,freq):
        self.write('FA %d'%freq)
    def set_stop_freq(self,freq):
        self.write('FB %d'%freq)
    def wait_for_opc(self):
        op_status_reg = self.query('*ESR?')
        print(op_status_reg)
        if (op_status_reg & 0x8):
            print("CURRENTLY SWEEPING")
    def plot_trace_a(self,filename_csv="",filename_image="",show_plot=0):
        #self.set_sweep_mode_single()
        sweep_time = self.get_sweep_time()
        print("sweep time: %f"%sweep_time)
        #self.sweep()
        #time.sleep(sweep_time)
        cf = float(self.get_center_frequency())
        rf_lvl = float(self.get_ref_level())
        mk_curr_freq = self.get_marker_frequency()
        self.marker_pk_search()
        # get marker values to get the compensation
        marker_freq_temp = self.get_marker_frequency()
        marker_temp_level = self.get_marker_level()
        self.set_marker_to_freq(mk_curr_freq)
        data_int = self.get_ascii_trace_data()
        print(np.max(data_int))
        print(np.min(data_int))
        span = int(float(self.get_span()))
        freqs = np.linspace(cf-span/2,cf+span/2,num=len(data_int))
        indx_marker = freqs.tolist().index(marker_freq_temp)

        data_int = np.array(data_int)
        print(indx_marker)
        print(data_int[indx_marker])


        slope = (rf_lvl-marker_temp_level)/(self.max_data_value-data_int[indx_marker])
        print(slope)

        intercept = marker_temp_level-slope*data_int[indx_marker]

        print(intercept)

        data_shifted = slope*np.array(data_int)+intercept

        print(np.max(data_shifted))
         
        plt.plot(freqs/1e6,data_shifted)
        if (show_plot==1):
            plt.ylabel("Magnitude (dBm)")
            plt.xlabel("Frequency (MHz)")
            plt.title("R3131 Raw Data Export")
            plt.show()

        if (filename_csv != ""):
            combined_array = np.zeros((len(freqs),2))
            combined_array[:,0]=freqs
            combined_array[:,1]=data_shifted
            np.savetxt(filename_csv,combined_array,fmt="%.5f",delimiter=',',header='Frequency (Hz), Magnitude (dBm)',comments='')
        
        if (filename_image != ""):
            plt.savefig(filename_image)

if __name__ == "__main__":
    r3131 = r3131_driver("10.2.0.9",8)
    r3131.get_idn_str()
