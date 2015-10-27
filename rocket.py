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
        '''Initialize an empty list to store measurements.
        Units measure the values in list.'''
        self.measure = []
        self.unit = unit

    def max(self, measure):
        'Return maximum value in the list'
        return max(int(meas) for meas in measure)

    def min(self, measure):
        'Return minimum value in the list'
        return round(min(float(meas) for meas in measure), 2)

    def avg(self, measure):
        'Return average value in the list'
        return round(sum(float(meas) for meas in measure) / (len(measure)), 1)

def parse_file(flight_file):
    'Open the file, read data in, & parse into arrays'
    open_file = open(flight_file, 'r')
    full_file = csv.reader(open_file)
    raw_data = [] # Empty list to put each line of the file into
    for row in full_file:
        for idx in row:
            match = re.search('^\d', idx) # Only want lines starting with digit
            if match and len(row) == 5:
                raw_data.append(row)
    flight_data = list(raw_data)
    # Create 5 empty arrays
    alti = Measurement('Altitude (ft)')
    time = Measurement('Time (sec)')
    velo = Measurement('Velocity (ft/sec)')
    temp = Measurement('Temperature (degrees F)')
    volt = Measurement('Voltage (V)')
    for x in range(len(flight_data)):
        time.measure.append(flight_data[x][0]) # For flight time readings
        alti.measure.append(flight_data[x][1]) # For altimeter height readings
        velo.measure.append(flight_data[x][2]) # For velocity readings
        temp.measure.append(flight_data[x][3]) # For ambient temperature readings
        volt.measure.append(flight_data[x][4]) # For battery voltage readings
    open_file.close()
    return alti, time, velo, temp, volt

# MAIN ROUTINE
while True:
    my_flight = select_flight()
    alti, time, velo, temp, volt = parse_file(my_flight)
    print('Maximum {}: {}'.format(alti.unit, alti.max(alti.measure)))
    print('Maximum {}: {}'.format(velo.unit, velo.max(velo.measure)))
    print('Average {}: {}'.format(temp.unit, temp.avg(temp.measure)))
    print('Minimum {}: {}'.format(volt.unit, volt.min(volt.measure)))

    # Plot altitude
    altitude = plt.figure()
    plt.plot(time.measure, alti.measure, label=alti.unit)
    plt.legend()
    plt.title(my_flight)
    altitude.canvas.set_window_title('Altitude Profile for ' + my_flight)

    # Plot velocity
    velocity = plt.figure()
    plt.plot(time.measure, velo.measure, label=velo.unit)
    plt.legend()
    plt.title(my_flight)
    velocity.canvas.set_window_title('Flight Velocity for ' + my_flight)

    # Plot temperature & battery voltage
    tempvolt = plt.figure()
    plt.plot(time.measure, temp.measure, label=temp.unit)
    plt.plot(time.measure, volt.measure, label=volt.unit)
    plt.legend()
    plt.title(my_flight)
    tempvolt.canvas.set_window_title('Temperature and Voltage for ' + my_flight)

    # Display plot windows
    plt.show()
