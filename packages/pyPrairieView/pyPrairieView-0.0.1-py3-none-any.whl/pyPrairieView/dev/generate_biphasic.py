#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 29 14:24:19 2022

@author: doug
"""

import numpy as np

# Set the sampling rate for the protocol (in Hz)
sampling_rate = 10e3

# Define the voltage levels for the biphasic protocol
voltage_levels = [-80, 80]

# Set the duration of each phase of the protocol (in seconds)
phase_duration = 0.5

# Set the inter-phase interval (in seconds)
inter_phase_interval = 0.1

# Set the number of repetitions of the protocol
n_reps = 5

# Create an empty list to store the voltage and time data
voltage_data = []
time_data = []

# Generate the biphasic protocol
for i in range(n_reps):
    for v in voltage_levels:
        # Calculate the number of samples for the phase duration
        n_samples = int(phase_duration * sampling_rate)
        # Append the voltage and time data to the lists
        voltage_data += [v] * n_samples
        time_data += [phase_duration] * n_samples
    # Calculate the number of samples for the inter-phase interval
    n_samples = int(inter_phase_interval * sampling_rate)
    # Append the voltage and time data to the lists
    voltage_data += [0] * n_samples
    time_data += [inter_phase_interval] * n_samples

# Convert the lists to NumPy arrays
voltage_data = np.array(voltage_data)
time_data = np.array(time_data)

# Combine the voltage and time data into a single NumPy array
protocol_data = np.vstack((time_data, voltage_data)).T
