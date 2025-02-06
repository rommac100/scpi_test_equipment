import pyvisa
import time

# ET5410 and other east tester load testing driver. Built off pyvisa (py-visa backend).
# Channel number notes. Channels are referred to "1" and "2" in integer forms i.e call function with channel =1 or 2
# a lot of time delays will be needed when a write is sent then a query of the same register is desired. try anywhere between 200ms and 1s
#
# Programming Manual from: https://www.eevblog.com/forum/testgear/east-tester-et5410-et5420-et5411-et54-series-software/?action=dlattach;attach=1030336
class et5410_driver:
    def __init__(self,resource_string):
        self.rm = pyvisa.ResourceManager()
        self.instr = self.rm.open_resource(resource_string)
        self.instr.read_termination = '\n'
        self.instr.write_termination = '\n'
        self.instr.baud_rate = 115200
        self.timeout = 20
        print(self.rm.list_resources())
    def get_idn_str(self):
        idn_str = self.query("*IDN?")
        print(idn_str)
        return idn_str
    def beep_instr(self):
        self.write(":BEEP")
    def query(self,command_str):
        self.write(command_str)
        time.sleep(.5)
        return self.read()
    def read(self):
        return self.instr.read() 
    def write(self,command_str):
        self.instr.write(command_str)
    # Utilities System
    def get_version(self):
        return self.query("SYSTEM:VERSION?")
    def get_current_baud_rate(self):
        return self.query("comm:baudrate?")
    # Current Subsystem
    def get_current_cc(self,channel):
        return self.query("CURR%d:CC?"%channel)
    def set_current_cc(self,channel,current):
        self.query("CURR%d:CC %.2f"%(channel,current))
    def set_max_current_protection(self,channel,max_current):
        self.query("CURR%d:IMAX %.2f"%(channel,max_current))
    def get_max_current_protection(self,channel):
        return self.query("CURR%d:IMAX?"%channel)
    # Voltage Subsystem
    def set_max_voltage_protection(self,channel,voltage_max):
        self.query("VOLT%d:VMAX %.2f"%(channel,voltage_max))
    def get_max_voltage_protection(self,channel):
        self.query("VOLT%d:VMAX"%(channel))
    def set_voltage_cv(self,channel,voltage):
        self.query("VOLT%d:CV %.2f"%(channel,voltage))
    # Measurement Subsystem
    def get_measured_voltage(self,channel):
        return self.query("MEAS%d:VOLTAGE?"%channel)
    def get_measured_current(self,channel):
        return self.query("MEAS%d:CURRENT?"%channel)
    # Battery Subsystem
    def set_mode_battery(self,channel,mode):
        self.query(":BATT%d:MODE %s"%(channel,mode))
    def get_mode_battery(self,channel):
        return self.query(":BATT%d:MODE?"%(channel))
    def get_battery_capacity(self,channel):
        return self.query(":BATT%d:CAPA?"%(channel))
    # Channel Subsystem
    def get_channel_mode(self,channel):
        return self.query(":CH%d:MODE?"%channel)
    def set_channel_mode(self,channel,channel_mode):
        print(self.query(":CH%d:MODE %s"%(channel,channel_mode)))
    def turn_on(self,channel):
        self.query(":CH%d:SW ON"%channel) 
    def turn_off(self,channel):
        self.query(":CH%d:SW OFF"%channel) 
    def get_on_state(self,channel):
        return self.query(":CH%d:SW?"%channel)

if __name__ == "__main__":
    et5410 = et5410_driver("ASRL/dev/ttyUSB0::INSTR")
    et5410.get_idn_str()
    # test channel 1 load
    et5410.turn_off(1)
    et5410.turn_off(2)
    time.sleep(1)
    print(et5410.get_on_state(1))
    et5410.set_channel_mode(1,"CC")
    time.sleep(1)
    print(et5410.get_channel_mode(1))
    et5410.set_current_cc(1,.25)
    et5410.set_max_current_protection(1,.5)
    et5410.set_max_voltage_protection(1,7)
    et5410.turn_on(1)
    time.sleep(2)
    print(et5410.get_measured_current(1))
    time.sleep(20)
    et5410.turn_off(1)
