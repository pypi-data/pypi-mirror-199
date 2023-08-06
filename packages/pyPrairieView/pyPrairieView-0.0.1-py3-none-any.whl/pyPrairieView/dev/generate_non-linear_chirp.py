#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 29 14:23:45 2022

@author: doug
"""

import numpy as np

# Set the sampling rate for the stimulus (in Hz)
sampling_rate = 10e3

# Define the start and end frequencies for the chirp
start_frequency = 1
end_frequency = 50

# Set the duration of the chirp (in seconds)
chirp_duration = 1.0

# Set the number of repetitions of the chirp
n_reps = 5

# Set the starting phase for the chirp
start_phase = 0

# Create an empty list to store the voltage and time data
voltage_data = []
time_data = []

# Generate the voltage chirp stimulus
for i in range(n_reps):
    # Calculate the number of samples in the chirp
    n_samples = int(chirp_duration * sampling_rate)
    # Generate a non-linear chirp of frequencies
    frequency_chirp = np.logspace(np.log10(start_frequency), np.log10(end_frequency), n_samples)
    # Calculate the time interval between each sample
    dt = chirp_duration / n_samples
    # Calculate the phase shift between each sample
    phase_shift = 2 * np.pi * frequency_chirp * dt
    # Calculate the cumulative phase shift
    phase = np.cumsum(phase_shift) + start_phase
    # Calculate the voltage values for the chirp
    voltage_chirp = np.sin(phase)
    # Append the voltage and time data to the lists
    voltage_data += list(voltage_chirp)
    time_data += [dt] * n_samples

# Convert the lists to NumPy arrays
voltage_data = np.array(voltage_data)
time_data = np.array(time_data)

# Combine the voltage and time data into a single NumPy array
stimulus_data = np.vstack((time_data, voltage_data)).T
