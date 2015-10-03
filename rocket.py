#! python3

import csv
import matplotlib.pyplot as plt
import sys

# Read second column of First_flight.pf2
flight_file = '2015-MAR-14_First_flight.pf2'
open_file = open(flight_file, 'r')
full_file = csv.reader(open_file)
raw_data = []
for row in full_file: # Strip out header lines by skipping them
    if full_file.line_num <= 15:
        continue
    raw_data.append(row)

flight_data = list(raw_data)
alt = [] # Empty array for storing altimeter height readings
time = [] # Empty array for storing flight time readings
velo = [] # Empty array for storing velocity readings
temp = [] # Empty array for ambient temperature readings
volt = [] # Empty array for battery voltage readings

# This is where the file needs to be read in & the (1st &) 2nd "words" in each
# column need to be appended into an array
for x in range(len(flight_data)):
    time.append(flight_data[x][0])
    alt.append(flight_data[x][1])
    velo.append(flight_data[x][2])
    temp.append(flight_data[x][3])
    volt.append(flight_data[x][4])

plt.plot(time, alt, label='Altitude(ft)')
plt.plot(time, velo, label='Velocity (ft/sec)')
plt.plot(time, temp, label='Ambient temp (F)')
plt.plot(time, volt, label='Battery Voltage (V)')
plt.legend()
plt.title(flight_file)
plt.show()
flight_file.close()
