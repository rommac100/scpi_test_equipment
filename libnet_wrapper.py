from libnienet import EnetLib
import struct
import matplotlib.pyplot as plt

class GPIBDriver:
    def __init__(self, host, addr):
        self.l = EnetLib(host)
        self.ud = self.l.ibdev(pad=addr, sad=0, tmo=10, eot=1, eos=0)

    def write(self, s):
        self.l.ibwrt(self.ud, s)

    def read_binary_data(self,s):
        self.write(s)
        data = self.read()
        data_out = bytearray()
        while (len(data) > 0):
            data_out.extend(data)
            data = self.read()

        return data_out

    def read(self):
        status, resp = self.l.ibrd(self.ud, 4096)
        return resp

    def query(self, s):
        self.write(s)
        return self.read()

if __name__ == "__main__":
    d = GPIBDriver("10.2.0.9", 8)
    print(d.query(b"*IDN?").decode())

    data_out = d.read_binary_data(b'TBA?')
    print(len(data_out))

    data_int = []
    data_int = struct.unpack_from(">"+"%dh"%(len(data_out)/2),data_out)
    plt.plot(data_int)
    plt.show()
    #print(data_int)
