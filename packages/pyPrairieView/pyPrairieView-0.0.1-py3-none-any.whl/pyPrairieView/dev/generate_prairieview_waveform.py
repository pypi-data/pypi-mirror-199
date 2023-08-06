# # Generating custom ephys protocols for use in PrairieView
# From PrairieView Help Menu (Main Control Window -> Electrophysiology Menut -> Voltage Output)): This is the most flexible component type since it allows the user to import a file containing any waveform definition.  The file must be an ASCII text file with a file extension of .txt or .csv.  Each line of the file defines one voltage preceded by one time duration (with units of milliseconds) to hold that voltage for.  The two values should be separated by a comma. Below is a simple example:
#        100, 2.5
#        400, 0
#        2000, 5 
#        1, 0 
# Importing a file with these contents would produce a waveform at 2.5 V for 100 ms, then change to 0 V for 400 ms, then 5 V for 2 seconds, and finally go back to 0 V for 1 ms.  If this were the last component in the waveform, the output would remain at the last voltage defined (in this case, 0 V).
# First column is the time duration
# Second column is the stimulus value (current or voltage injection)
# 
# TO-DO
# 1. add option to convert to make it appear like episodic stimulation
# 2. Name for waveform
# 3. Interstep interval
# 4. Step size (delta)
# 5. Holding value
# 6. 

def generate_prairieview_stimulus(recording_type, duration=30, span_sec=10, rate=10000, holding=-70, amplitude=10, display=True):
    """
    Generates a waveform that is scaled to clamp cells under specified conditions. If the output is displayed, this will be scaled to the actual clamp units, not the scaled ones for the amplifier.
    
    inputs:
        duration - time in seconds for the duration of the recording
        rate - number of samples/second for the recording
        holding - amount of current/voltage to hold the cell at
        
    """
    # import dependencies
    import matplotlib.pyplot as plt
    import numpy as np
    
    # pClamp order of tabs
        # mode/rate
        # inputs
        # outputs
        # trigger
        # statistics
        # comments
        # math
        # waveform
        # stimulus
        
    # type - voltage, current
    # mode - ramp, step, pulse, 
    # Generate the temporal component
    recording_time = np.zeros(rate*duration)
    # Convert the rate to the interval in seconds, multiply by 1000 to convert to ms
    time_interval = (1/rate*1000) 
    for row in recording_time:
        recording_time[row]=time_interval
    # Generate name -> recording modality 
    # Interstep interval
    # Step size
    # Holding
    match recording_type:
        case "voltage": 
            # make a voltage protocol
            command_wave = np.zeros(rate*duration)
        case "current": 
            # make a current protocol
            command_wave = np.zeros(rate*duration)
            # make a current protocol
            
    if display:
        
        display_time = recording_time
        for row in display_time:
            display_time[row] = time_interval + (row*time_interval)
            
        plt.figure(figsize=(8,4))
        plt.title("Generated protocol")
        if not 'clamp_type' in locals():
            clamp_type = "None"  
        else:
            print("success, clamp type was specified")
            
        if clamp_type == current:
            plt.ylabel("pA")
        elif clamp_type == "voltage":
            plt.ylabel("mV")
        else:
            plt.ylabel('pA or mV - clamp_type not specified - please fix')
        plt.plot(display_time,data)
        plt.axhline(holding,color='r',alpha=.2,ls='--')

        plt.xlabel("Stimulus Time (seconds)")
        plt.tight_layout()
        plt.margins(0.02,.1)
        #plt.savefig("sine-sweep.png",dpi=100)
        plt.show()