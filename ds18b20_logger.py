import os
import glob
import time
import datetime
import csv

#these tow lines mount the device:
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
 
class DS18B20:
    def __init__(self):
        self.base_dir = r'/sys/bus/w1/devices/28*'
        self.sensor_path = []        
        self.sensor_name = []
        self.temps = []
        self.rows = []

    def find_sensors(self):
        self.sensor_path = glob.glob(self.base_dir)
        self.sensor_name = [path.split('/')[-1] for path in self.sensor_path]

    def strip_string(self, temp_str):
        i = temp_str.index('t=')
        if i != -1:
            t = temp_str[i+2:]
            temp_c = float(t)/1000.0
            temp_f = temp_c * (9.0/5.0) + 32.0
        return temp_c, temp_f

    def read_temp(self):
        tstamp = datetime.datetime.now()
        for sensor, path in zip(self.sensor_name, self.sensor_path):
            # open sensor file and read data
            with open(path + '/w1_slave','r') as f:
                valid, temp = f.readlines()
            # check validity of data
            if 'YES' in valid:
                self.rows.append((tstamp, sensor) + self.strip_string(temp))
                time.sleep(2)
            else:
                time.sleep(0.2)
    
    def print_temps(self):
        print('-'*90)
        for t, n, c, f in self.rows:
            print(f'Sensor: {n}  C={c:,.3f}  F={f:,.3f}  DateTime: {t}')
            
    def log_csv(self):
        with open('log.csv','a+') as log:
            writer = csv.writer(log)
            writer.writerows(self.rows)

    def clear_rows(self):
        self.rows.clear()

s = DS18B20()
s.find_sensors()

while True:
    s.read_temp()
    s.print_temps()
    s.log_csv()
    s.clear_rows()
