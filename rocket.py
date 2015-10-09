#! python3

import csv
import glob
import matplotlib.pyplot as plt
import os
import re
import sys
import time

while True:
    print('Perfectflite files found in current directory (' + os.getcwd() + '):')
    count = 0
    for file in glob.glob('*.pf2'):
        count += 1
        print('    ' + str(count) + '. ' + file)
    selection = int(input('Enter the number next of filename that you would like to plot a chart for: '))
    if selection < 1 or selection > count:
        print('Invalid selection. Please try again...')
        time.sleep(2)
        continue
    else:
        flight_file = file
        counter = 0
        for file in glob.glob('*.pf2'):
            counter += 1
            if counter == selection:
                print('You selected ' + flight_file)
                break # Break for loop
        break # Break while loop

# Open the file, parse into arrays, & display chart
open_file = open(flight_file, 'r')
full_file = csv.reader(open_file)
raw_data = [] # Empty array to put each line of the file into
for row in full_file: # Iterate through each row
    for idx in row: #Iterate through each element
        match = re.search('^\d', idx) # Only want lines that start with a digit
        if match: # Fields found will be added to list
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
open_file.close()
sys.exit(0)
