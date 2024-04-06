from r3131_driver import r3131_driver
import time
filename = "test_loss_data.csv"

max_time_s = 60*60
sample_period = 60

r3131 = r3131_driver("10.2.0.9",8)
r3131.get_idn_str()
