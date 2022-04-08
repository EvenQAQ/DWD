import argparse
import datetime
from time import sleep
parser = argparse.ArgumentParser()
parser.add_argument("-p", "--position", type=int, default=3)
args = parser.parse_args()
rotor_last = args.position
rotor_now = rotor_last + 1
print(rotor_last)
print(rotor_now)


starttime = datetime.datetime.now()
#long running
sleep(2)
endtime = datetime.datetime.now()
print((endtime - starttime).seconds)
