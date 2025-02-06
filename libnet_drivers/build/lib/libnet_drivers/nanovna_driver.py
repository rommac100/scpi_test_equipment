from skrf.vi import vna
import skrf as rf
from matplotlib import pyplot as plt

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
    def get_device_info(self):
        return self.nanovna.device_info

if __name__ == '__main__':
    nanovna = nanovna_driver('ASRL/dev/ttyACM0::INSTR')
    #nanovna.set_start_freq(100e6)
    #nanovna.set_stop_freq(1e9)
    nanovna.set_npoints(100)
    #nanovna.set_step_hz(1e6)
    #data = nanovna.get_s21()
    #print(data)
    #data.plot_s_db()
    #plt.show()
    print(nanovna.nanovna.device_info)
