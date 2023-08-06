# # Generating custom ephys protocols for use in PrairieView
# From PrairieView Help Menu (Main Control Window -> Electrophysiology Menut -> Voltage Output)): This is the most flexible component type since it allows the user to import a file containing any waveform definition.  The file must be an ASCII text file with a file extension of .txt or .csv.  Each line of the file defines one voltage preceded by one time duration (with units of milliseconds) to hold that voltage for.  The two values should be separated by a comma. Below is a simple example:
#        100, 2.5
#        400, 0
#        2000, 5 
#        1, 0 
# Importing a file with these contents would produce a waveform at 2.5 V for 100 ms, then change to 0 V for 400 ms, then 5 V for 2 seconds, and finally go back to 0 V for 1 ms.  If this were the last component in the waveform, the output would remain at the last voltage defined (in this case, 0 V).
# Chances are that the scaling will have to be adjusted for the amplifier

# Specify the duration of the recording


# Specify the sampling rate


# Generate name -> recording modality 