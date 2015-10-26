#!/usr/bin/python3

import csv
import glob
import matplotlib.pyplot as plt
import os
import re
import sys
import time

def errmsgslow(text):
    'Prints message to screen then pauses for 2 seconds.'
    print(text)
    time.sleep(2)

def select_flight():
    'Lists all .pf2 files in currently directory & prompts user to select one.'
    while True:
        print('''Current directory is:
\t{}
Perfectflite files found:'''.format(os.getcwd()))
        count = 0
        for files in glob.glob('*.pf2'):
            count += 1
            print('\t{}. {}'.format(count, files))
        print('\tX. Exit')
        selection = input('Enter the number of the file you want to plot or exit: ')
        if selection.lower() == 'x':
            print('Exiting Rocket Flight Plotter...')
            sys.exit(0)
        elif not selection.isnumeric():
            errmsgslow('Invalid selection. Please try again...')
            continue
        elif int(selection) < 1 or int(selection) > count:
            errmsgslow('Invalid selection. Please try again...')
            continue
        else:
            flight_file = files
            counter = 0
            for files in glob.glob('*.pf2'):
                counter += 1
                if counter == int(selection):
                    print('You selected {}'.format(flight_file))
                    return flight_file
                    break # Break for loop
                break # Break while loop

class Measurement:
    def __init__(self, unit):
        'Comment goes here'
        measure = []
        self.unit = unit

    def max(self, measure):
        'Return maximum value in the list'
        return max(int(meas) for meas in measure)

    def min(self, measure):
        'Return minimum value in the list'
        return min(int(meas) for meas in measure)

    def avg(self, measure):
        'Return average value in the list'
        return round(sum(float(meas) for meas in measure) / (len(measure), 1)

def parse_file(flight_file):
    'Open the file, read data in, & parse into arrays'
    open_file = open(flight_file, 'r')
    full_file = csv.reader(open_file)
    raw_data = [] # Empty list to put each line of the file into
    for row in full_file: # Iterate through each row
        for idx in row: #Iterate through each element
            match = re.search('^\d', idx) # Only want lines starting with digit
            if match and len(row) == 5: # Fields found will be added to list
                raw_data.append(row)
    flight_data = list(raw_data)
    # Create 5 empty arrays
    alti = Measurement('Altitude (ft)')
    time = Measurement('Time (sec)')
    velo = Measurement('Velocity (ft/sec)')
    temp = Measurement('Temperature (degrees F)')
    volt = Measurement('Voltage (V)')
    for x in range(len(flight_data)):
        time.append(flight_data[x][0]) # For flight time readings
        alti.append(flight_data[x][1]) # For altimeter height readings
        velo.append(flight_data[x][2]) # For velocity readings
        temp.append(flight_data[x][3]) # For ambient temperature readings
        volt.append(flight_data[x][4]) # For battery voltage readings
    open_file.close()
    return alti, time, velo, temp, volt

# MAIN ROUTINE
while True:
    my_flight = select_flight()
    a, t, s, d, b = parse_file(my_flight)
    peak_alt = max(int(ht) for ht in a)
    max_velo = max(int(spd) for spd in s)
    avg_temp = round(sum(float(deg) for deg in d) / len(d), 1)
    min_volt = min(float(bat) for bat in b)
    print('Maximum altitude:    {}ft'.format(peak_alt))
    print('Maximum velocity:    {}ft/sec'.format(max_velo))
    print('Average temperature: {} degrees F'.format(avg_temp))
    print('Minimum voltage:     {}V'.format(min_volt))

    # Show altitude
    altitude = plt.figure()
    plt.plot(t, a, label='Altitude(ft)')
    plt.legend()
    plt.title(my_flight)
    altitude.canvas.set_window_title('Altitude Profile for ' + my_flight)

    # Show velocity
    velocity = plt.figure()
    plt.plot(t, s, label='Velocity (ft/sec)')
    plt.legend()
    plt.title(my_flight)
    velocity.canvas.set_window_title('Flight Velocity for ' + my_flight)

    # Show temperature & battery voltage
    tempvolt = plt.figure()
    plt.plot(t, d, label='Ambient temp (F)')
    plt.plot(t, b, label='Battery Voltage (V)')
    plt.legend()
    plt.title(my_flight)
    tempvolt.canvas.set_window_title('Temperature and Voltage for ' + my_flight)
    plt.show()
