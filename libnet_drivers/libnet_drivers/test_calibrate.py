import skrf
from skrf.calibration import TwoPortOnePath, OnePort
from nanovna_driver import nanovna_driver
from matplotlib import pyplot as plt

short_raw = skrf.Network("/mnt/main_documents/lab_data/cal_standard/test/SHORT.s1p")
#short_raw = skrf.two_port_reflect(short_raw,short_raw)
open_raw = skrf.Network("/mnt/main_documents/lab_data/cal_standard/test/OPEN.s1p")
#open_raw = skrf.two_port_reflect(open_raw,open_raw)
load_raw = skrf.Network("/mnt/main_documents/lab_data/cal_standard/test/LOAD.s1p")
#load_raw = skrf.two_port_reflect(load_raw,load_raw)

line = skrf.DefinedGammaZ0(frequency=short_raw.frequency,z0=50)

cal = OnePort(ideals=[line.short(nports=1),line.open(nports=1),line.match(nports=1)],measured=[short_raw,open_raw,load_raw])

cal.run()


nanovna = nanovna_driver('ASRL/dev/ttyACM0::INSTR')
nanovna.set_start_freq(1e6)
nanovna.set_stop_freq(1e9)
nanovna.set_step_hz(1e6)

s11 = nanovna.get_s11()
s11_calibrated = cal.apply_cal(s11)

s11_calibrated.plot_s_db(0,0)
plt.ylim([-.03,.02])
plt.show()
