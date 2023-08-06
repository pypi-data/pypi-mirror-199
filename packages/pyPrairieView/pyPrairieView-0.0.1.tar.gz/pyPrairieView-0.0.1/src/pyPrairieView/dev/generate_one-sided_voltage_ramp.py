#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 29 14:21:45 2022

@author: doug
"""

import numpy as np

# Set the sampling rate for the protocol (in Hz)
sampling_rate = 10e3

# Define the start and end voltage levels for the ramp
start_voltage = -80
end_voltage = 80

# Set the duration of the ramp (in seconds)
ramp_duration = 1.0

# Set the number of repetitions of the protocol
n_reps = 5

# Create an empty list to store the voltage and time data
voltage_data = []
time_data = []

# Generate the voltage ramp protocol
for i in range(n_reps):
    # Calculate the number of samples in the ramp
    n_samples = int(ramp_duration * sampling_rate)
    # Generate a linear ramp of voltage values
    voltage_ramp = np.linspace(start_voltage, end_voltage, n_samples)
    # Calculate the time interval between each sample
    dt = ramp_duration / n_samples
    # Append the voltage and time data to the lists
    voltage_data += list(voltage_ramp)
    time_data += [dt] * n_samples

# Convert the lists to NumPy arrays
voltage_data = np.array(voltage_data)
time_data = np.array(time_data)

# Combine the voltage and time data into a single NumPy array
protocol_data = np.vstack((time_data, voltage_data)).T
