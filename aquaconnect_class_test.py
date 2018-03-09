import time
from aqjsonpy.controller import Controller

pool = Controller('192.168.1.15', 6)
time.sleep(5)
pool.switches[5].toggle()
time.sleep(5)
pool.switches[5].toggle()
