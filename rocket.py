#! python3

import csv
import glob
import matplotlib.pyplot as plt
import os
import re
import sys
import time

def select_flight():
    'Lists all .pf2 files in currently directory & prompts user to select one.'
    while True:
        print('Perfectflite files found in current directory (' + os.getcwd() + '):')
        count = 0
        for file in glob.glob('*.pf2'):
            count += 1
            print('    ' + str(count) + '. ' + file)
            print('    X. Exit')
        selection = input('Enter the number of the file you want to plot or exit: ')
        if selection.lower() == 'x':
            print('Exiting Rocket Flight Plotter...')
            sys.exit(0)
        elif not selection.isnumeric():
            print('Invalid selection. Please try again...')
            time.sleep(2)
            continue
        elif int(selection) < 1 or int(selection) > count:
            print('Invalid selection. Please try again...')
            time.sleep(2)
            continue
        else:
            flight_file = file
            counter = 0
            for file in glob.glob('*.pf2'):
                counter += 1
                if counter == int(selection):
                    print('You selected ' + flight_file)
                    return flight_file
                    break # Break for loop
                break # Break while loop

def parse_file(flight_file):
    'Open the file, read data in, & parse into arrays'
    open_file = open(flight_file, 'r')
    full_file = csv.reader(open_file)
    raw_data = [] # Empty array to put each line of the file into
    for row in full_file: # Iterate through each row
        for idx in row: #Iterate through each element
            match = re.search('^\d', idx) # Only want lines starting with digit
            if match: # Fields found will be added to list
                raw_data.append(row)
    flight_data = list(raw_data)
    # Create 5 empty arrays
    alti = [] # For altimeter height readings
    time = [] # For flight time readings
    velo = [] # For velocity readings
    temp = [] # For ambient temperature readings
    volt = [] # For battery voltage readings
    for x in range(len(flight_data)):
        time.append(flight_data[x][0])
        alti.append(flight_data[x][1])
        velo.append(flight_data[x][2])
        temp.append(flight_data[x][3])
        volt.append(flight_data[x][4])
    open_file.close()
    return alti, time, velo, temp, volt

# MAIN ROUTINE
while True:
    my_flight = select_flight()
    a, t, s, d, b = parse_file(my_flight)

    # Show altitude
    plt.plot(t, a, label='Altitude(ft)')
    plt.legend()
    plt.title(my_flight)
    plt.show()

    # Show velocity
    plt.plot(t, s, label='Velocity (ft/sec)')
    plt.legend()
    plt.title(my_flight)
    plt.show()

    # Show temperature & battery voltage
    plt.plot(t, d, label='Ambient temp (F)')
    plt.plot(t, b, label='Battery Voltage (V)')
    plt.legend()
    plt.title(my_flight)
    plt.show()
