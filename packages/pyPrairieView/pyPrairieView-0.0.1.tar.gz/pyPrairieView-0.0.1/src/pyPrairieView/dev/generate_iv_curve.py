#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 29 14:25:01 2022

@author: doug
"""

import numpy as np
import matplotlib.pyplot as plt

# Set the sampling rate for the protocol (in Hz)
sampling_rate = 10e3

# Set the holding potential
holding_potential = -70

# Define the voltage levels for the intrinsic neuronal property protocol
voltage_levels = [-80, -70, -60, -50, -40, -30, -20, -10, 0, 10, 20, 30, 40, 50, 60, 70, 80]

# Set the duration of each phase of the protocol (in seconds)
phase_duration = 0.5

# Set the inter-stimulus interval(in seconds)
inter_stimulus_interval = 0.25

# Set the inter-phase interval (in seconds)
inter_phase_interval = 0.1

# Set the number of repetitions of the protocol
n_reps = 3

# Create an empty list to store the voltage and time data
voltage_data = []
time_data = []

# Generate the intrinsic neuronal property protocol
for i in range(n_reps):
    for v in voltage_levels:
        # Calculate the number of samples for the phase duration
        n_samples = int(phase_duration * sampling_rate)
        isi_samples = int(inter_stimulus_interval * sampling_rate)
        # Append the voltage and time data to the lists
        voltage_data += [v] * n_samples
        voltage_data += [holding_potential] * isi_samples
        time_data += [phase_duration] * n_samples
        time_data += [inter_phase_interval] * isi_samples
    # Calculate the number of samples for the inter-phase interval
    n_samples = int(inter_phase_interval * sampling_rate)
    # Append the voltage and time data to the lists
    voltage_data += [holding_potential] * n_samples
    time_data += [inter_phase_interval] * n_samples

# Convert the lists to NumPy arrays
voltage_data = np.array(voltage_data)
time_data = np.array(time_data)

# Combine the voltage and time data into a single NumPy array
protocol_data = np.vstack((time_data, voltage_data)).T

temporal_position = np.linspace(start=0, stop=(len(voltage_data) / sampling_rate), num=(len(voltage_data)))

fig, axes = plt.subplots()
axes.plot(temporal_position, voltage_data)
axes.set (xlabel = 'Time (s)', ylabel ='Voltage (mV)', title = "Voltage Clamp I/V Curve Protocol")
axes.spines['top'].set_visible(False)
axes.spines['right'].set_visible(False)

fig.show
