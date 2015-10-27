#!/usr/bin/python3

import csv
import glob
import matplotlib.pyplot as plt
import os
import re
import sys
import time

class Measurement:
    def __init__(self, unit, title):
        '''Initialize an empty list to store measurements.
        Units measure the values in list.'''
        self.measure = []
        self.unit = unit
        self.title = title

    def max(self):
        'Return maximum value in the list'
        return max(int(meas) for meas in self.measure)

    def min(self):
        'Return minimum value in the list'
        return round(min(float(meas) for meas in self.measure), 2)

    def avg(self):
        'Return average value in the list'
        return round(sum(float(meas) for meas in self.measure) / (len(self.measure)), 1)

class ChartElement:
    def __init__(self, x, y, legend, plot_file, title):
        'Gather all elements necessary to plot a chart'
        self.x = x
        self.y = y
        self.legend = legend
        self.plot_file = plot_file
        self.title = title
        plt.figure().canvas.set_window_title(self.title + ' for ' + self.plot_file)
        plt.plot(self.x, self.y, label=self.legend)
        plt.legend()
        plt.title(self.plot_file)

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
    alti = Measurement('Altitude (ft)', 'Altitude Profile')
    time = Measurement('Time (sec)', '')
    velo = Measurement('Velocity (ft/sec)', 'Flight Velocity')
    temp = Measurement('Temperature (degrees F)', 'Ambient Temperature')
    volt = Measurement('Voltage (V)', 'Battery Voltage')
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
    print('Maximum {}: {}'.format(alti.unit, alti.max()))
    print('Maximum {}: {}'.format(velo.unit, velo.max()))
    print('Average {}: {}'.format(temp.unit, temp.avg()))
    print('Minimum {}: {}'.format(volt.unit, volt.min()))

    # Plot altitude
    altitude = ChartElement(time.measure, alti.measure, alti.unit, my_flight, alti.title)

    # Plot velocity
    velocity = ChartElement(time.measure, velo.measure, velo.unit, my_flight, velo.title)

    # Plot temperature
    temperature = ChartElement(time.measure, temp.measure, temp.unit, my_flight, temp.title)

    # Plot battery voltage
    voltage = ChartElement(time.measure, volt.measure, volt.unit, my_flight, volt.title)

    # Display plot windows
    plt.show()
