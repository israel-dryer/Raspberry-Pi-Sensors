import os
import glob
import time
import csv
from datetime import datetime

#these tow lines mount the device:
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
 
base_dir = '/sys/bus/w1/devices/'
device_path = glob.glob(base_dir + '28*') #get list of file paths of sensors
rom = [d.split('/')[-1] for d in device_path] #get list of roms

def read_temp_raw(i):
    with open(device_path[i] +'/w1_slave','r') as f:
        valid, temp = f.readlines()
    return valid, temp

def log_temp(r, c, f):
    with open('log.csv','a+') as log:
        timestamp = datetime.now()
        row = [timestamp, r, c, f] 
        # write the data to csv
        writer = csv.writer(log)
        writer.writerow(row)
        
 
def read_temp():
    
    for i in range(len(rom)):
        
        valid, temp = read_temp_raw(i)
        print('ROM: ' + rom[i])
        while 'YES' not in valid:
            time.sleep(0.2)
            valid, temp = read_temp_raw()

        pos = temp.index('t=')
        if pos != -1:
            #read the temperature .
            temp_string = temp[pos+2:]
            temp_c = float(temp_string)/1000.0 
            temp_f = temp_c * (9.0 / 5.0) + 32.0
            return rom[i], temp_c, temp_f
 
while True:
    r, c, f = read_temp()
    # log the results into csv
    log_temp(r, c, f)
    # print the results
    print(' C={:,.3f} F={:,.3f}\n'.format(c, f))

    time.sleep(1)
