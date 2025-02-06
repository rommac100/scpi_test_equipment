import pyvisa
import time

class dg822_driver:
    def __init__(self,resource_string):
        self.rm = pyvisa.ResourceManager()
        #self.instr = self.rm.open_resource(resource_string)
        #self.instr.read_termination = '\n'
        #self.instr.write_termination = '\n'
        #self.instr.baud_rate = 115200
        #self.timeout = 20
        print(self.rm.list_resources())

if __name__ == "__main__":
   test = dg822_driver("test") 
