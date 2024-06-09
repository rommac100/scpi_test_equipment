from skrf.vi import vna
import skrf as rf
from matplotlib import pyplot as plt
from enum import Enum

class IFBW(bytes, Enum):
    IFBW_800HZ = b"\x05"
    IFBW_1700HZ = b"\x0a"
    IFBW_3100HZ = b"\x14"
    IFBW_4700HZ = b"\x1e"
    IFBW_6200HZ = b"\x28"
    IFBW_10000HZ = b"\x3c"

# uses skrf basis for the class but adds additional features as needed
class nanovna_driver:
    def __init__(self,instrument_resource):
        self.nanovna = rf.vi.vna.nanovna.NanoVNA(instrument_resource)
    def set_start_freq(self,freq_hz):
        self.nanovna.freq_start = freq_hz
    def set_stop_freq(self,freq_hz):
        self.nanovna.freq_stop = freq_hz
    def set_npoints(self,npoints):
        self.nanovna.npoints = npoints
    def set_step_hz(self,hz_step):
        self.set_npoints(int((self.nanovna.freq_stop-self.nanovna.freq_start)/hz_step))
    def get_s11_s21_data(self):
        return self.nanovna.get_s11_s21()
    def get_s11(self):
        s11,s21 = self.get_s11_s21_data()
        return s11
    def get_s21(self):
        s11,s21 = self.get_s11_s21_data()
        return s21
    def set_if_bw(self,ifbw : IFBW):
        print("setting ifbw")
        cmd = b"\x20" + b"\x42" + b"\x28"
        self.nanovna.write_raw(cmd)
        cmd = b"\x20" + b"\x42" + ifbw
        self.nanovna.write_raw(cmd)
    def get_if_bw(self):
        print('getting ifbw')
        cmd = b"\x10" + b"\x42"
        self.nanovna.write_raw(cmd)
        data = self.nanovna.read_bytes(1)
        data = int.from_bytes(data)
        return data
    def get_device_info(self):
        return self.nanovna.device_info
    def perform_1port_cal(self,output_directory):
        paths_to_test = ["SHORT","OPEN","LOAD"]
        for path in paths_to_test:
            input("Put the following standard on: %s"%path)
            data = self.get_s11()
            data.write_touchstone("%s.s1p"%(output_directory+path),form='db')
    def perform_full_cal(self,output_directory): # goes through the various configurations and offloads the data to the designated folder
        print("performing full cal")
        paths_to_test = ["SHORT","OPEN","LOAD",'THRU']
        for path in paths_to_test:
            input("Put the following standard on: %s"%path)
            if (path != "THRU"):
                data = self.get_s11()
                data.write_touchstone("%s.s1p"%(output_directory+path),form='db')
            else:
                s11,s21 = self.get_s11_s21_data()
                #data.write_touchstone("%s.s2p"%(output_directory+path),form='db')


if __name__ == '__main__':
    nanovna = nanovna_driver('ASRL/dev/ttyDUM::INSTR')
    nanovna.set_if_bw(IFBW.IFBW_1700HZ)
    nanovna.get_if_bw()
    #nanovna.set_npoints(60)
    #nanovna.set_start_freq(1e6)
    #nanovna.set_stop_freq(1e9)
    #nanovna.set_step_hz(1e6)
    #nanovna.perform_1port_cal("/mnt/main_documents/lab_data/cal_standard/test/")
