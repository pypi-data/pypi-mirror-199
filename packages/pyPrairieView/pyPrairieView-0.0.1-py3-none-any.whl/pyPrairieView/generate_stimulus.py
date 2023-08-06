"""A library of functions for generating stimuli."""
def generate_chirp_stimulus(freq_max_hz=10,
                            span_sec=10,
                            rate=10000,
                            holding=-70,
                            amplitude=10,
                            display=False,
                            clamp_type=None,
                            save_figure=False,
                            save_csv=False):
    """Generate a chirp stimulus of increasing frequency.

    Waveform is padded with 1 second of zeros on both sides. Returns an array
    (scaled -1 to 1) of a sine wave of increasing frequency.The frequency
    increases linearly. Zero-intercepts can also be calculated.

    Args:
        freq_max_hz (int): Maximum frequency of signal oscillation
        span_sec (int): Amount of time in seconds the frequency increases
        rate (int): Sampling rate of the digitizer
        holing (int): Baseline value around which oscillation occurs
        amplitude (int): Peak change around holding value
        clamp_type (str): Type of clamp being executed ('current' or 'voltage')

    Returns:
        data_full (np.array): A 2xM numpy array of the stimulus, [0] is holding duration, [1] stimulus
    
    """
    import matplotlib.pyplot as plt
    import numpy as np
    # initialize variables

    # generate sine wave
    time_scale = freq_max_hz/span_sec/2
    Xs = np.arange(rate*span_sec)/rate
    zi = np.sqrt(np.arange(0, (Xs[-1]**2)*time_scale, 1)/time_scale)
    cycle_freqs = np.concatenate(([0], 1/np.diff(zi)))
    data = np.sin(2*np.pi*(Xs**2)*time_scale)
    data = data*amplitude
    data = data+holding

    if display:
        plt.figure(figsize=(8, 4))
        ax1 = plt.subplot(211)
        plt.title("Sine Sweep (0.00 - %.02f Hz)" % (freq_max_hz))
        if clamp_type == 'current':
            plt.ylabel('pA')
        elif clamp_type == 'voltage':
            plt.ylabel('mV')
        else:
            plt.ylabel("mV or pA")
        plt.plot(Xs, data)
        plt.axhline(holding, color='r', alpha=.2, ls='--')
        plt.subplot(212, sharex=ax1)
        plt.ylabel("Frequency (Hz)")
        plt.xlabel("Stimulus Time (seconds)")
        plt.plot(zi, cycle_freqs, '.-')
        plt.tight_layout()
        plt.margins(0.02, .1)
        if save_figure is True:
            plt.savefig("sine-sweep.png", dpi=300)
        plt.show()

    # pad on both sides with 1 second of zeros
    data = np.concatenate((np.zeros(rate)+holding, data, np.zeros(rate)+holding))
    x = np.arange(len(data), dtype=int)
    holding_time = np.full_like(x, 1/rate*1000, dtype=np.double)
    data_full = np.column_stack((holding_time, data))
    if save_csv is True:
        np.savetxt("sine_sweep_%0.02f.csv" % (freq_max_hz),
                   data_full,
                   delimiter=",")
    return data_full, freq_max_hz



def generate_ap_stimulus(rate=10000, resting_potential=-70, tmin=0.0, tmax=50.0, input_stimulus=100, save_csv=False):
    """Generate action potential waveforms.

    Args:

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    import matplotlib.pyplot as plt
    import numpy as np

    from scipy.integrate import odeint

    # Set random seed (for reproducibility)
    np.random.seed(1000)

    # Start and end time (in milliseconds)
    tmin = tmin
    tmax = tmax

    # Average potassium channel conductance per unit area (mS/cm^2)
    gK = 36.0

    # Average sodoum channel conductance per unit area (mS/cm^2)
    gNa = 120.0

    # Average leak channel conductance per unit area (mS/cm^2)
    gL = 0.3

    # Membrane capacitance per unit area (uF/cm^2)
    Cm = 1.0

    # Potassium potential (mV)
    VK = -12.0

    # Sodium potential (mV)
    VNa = 115.0

    # Leak potential (mV)
    Vl = 10.613

    # Time values
    T = np.linspace(tmin, tmax, rate)

    # Potassium ion-channel rate functions

    def alpha_n(Vm):
        return (0.01 * (10.0 - Vm)) / (np.exp(1.0 - (0.1 * Vm)) - 1.0)

    def beta_n(Vm):
        return 0.125 * np.exp(-Vm / 80.0)

    # Sodium ion-channel rate functions

    def alpha_m(Vm):
        return (0.1 * (25.0 - Vm)) / (np.exp(2.5 - (0.1 * Vm)) - 1.0)

    def beta_m(Vm):
        return 4.0 * np.exp(-Vm / 18.0)

    def alpha_h(Vm):
        return 0.07 * np.exp(-Vm / 20.0)

    def beta_h(Vm):
        return 1.0 / (np.exp(3.0 - (0.1 * Vm)) + 1.0)

    # n, m, and h steady-state values

    def n_inf(Vm=0.0):
        return alpha_n(Vm) / (alpha_n(Vm) + beta_n(Vm))

    def m_inf(Vm=0.0):
        return alpha_m(Vm) / (alpha_m(Vm) + beta_m(Vm))

    def h_inf(Vm=0.0):
        return alpha_h(Vm) / (alpha_h(Vm) + beta_h(Vm))

    # Input stimulus
    def Id(t):
        if 10.0 < t < 10.5:
            return input_stimulus
        # elif 10.0 < t < 11.0:
        #     return 50.0
        return 0.0

    # Compute derivatives
    def compute_derivatives(y, t0):
        dy = np.zeros((4,))

        Vm = y[0]
        n = y[1]
        m = y[2]
        h = y[3]

        # dVm/dt
        GK = (gK / Cm) * np.power(n, 4.0)
        GNa = (gNa / Cm) * np.power(m, 3.0) * h
        GL = gL / Cm

        dy[0] = (Id(t0) / Cm) - (GK * (Vm - VK)) - (GNa * (Vm - VNa)) - (GL * (Vm - Vl))

        # dn/dt
        dy[1] = (alpha_n(Vm) * (1.0 - n)) - (beta_n(Vm) * n)

        # dm/dt
        dy[2] = (alpha_m(Vm) * (1.0 - m)) - (beta_m(Vm) * m)

        # dh/dt
        dy[3] = (alpha_h(Vm) * (1.0 - h)) - (beta_h(Vm) * h)

        return dy

    # State (Vm, n, m, h)
    Y = np.array([0.0, n_inf(), m_inf(), h_inf()])

    # Solve ODE system
    # Vy = (Vm[t0:tmax], n[t0:tmax], m[t0:tmax], h[t0:tmax])
    Vy = odeint(compute_derivatives, Y, T)
    Vy = Vy - (abs(resting_potential))
    # Input stimulus
    Idv = [Id(t) for t in T]

    fig, ax = plt.subplots(figsize=(12, 7))
    ax.plot(T, Idv)
    ax.set_xlabel('Time (ms)')
    ax.set_ylabel(r'Current density (uA/$cm^2$)')
    ax.set_title('Stimulus (Current density)')
    plt.grid()

    # Neuron potential
    fig, ax = plt.subplots(figsize=(12, 7))
    ax.plot(T, Vy[:, 0])
    ax.set_xlabel('Time (ms)')
    ax.set_ylabel('Membrane potential (mV)')
    ax.set_title('Synthetic action potenial')
    plt.grid()

    # Trajectories with limit cycles
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.plot(Vy[:, 0], Vy[:, 1], label='Vm - n')
    ax.plot(Vy[:, 0], Vy[:, 2], label='Vm - m')
    ax.set_title('Limit cycles')
    ax.legend()
    plt.grid()
    if save_csv is True:
        x = np.arange(len(Vy[:, 0]), dtype=int)
        holding_time = np.full_like(x, 1/rate, dtype=np.double)
        data_full = np.column_stack((holding_time, Vy[:, 0]))
        np.savetxt("ap_sweep.csv",
                   data_full,
                   delimiter=",")
    return Vy[:, 0]

# Voltage Ramp Protocol

def generate_voltage_ramp(start_voltage=-70, end_voltage=-80, ramp_duration=0.1, sampling_rate=10e3, display_protocol=False, save_csv=False):
    import numpy as np
    import matplotlib.pyplot as plt
    
    # Set the sampling rate for the protocol (in Hz)
    sampling_rate = 10e3
    
    # Define the start and end voltage levels for the ramp
    start_voltage = start_voltage
    end_voltage = end_voltage
    
    # Set the duration of the ramp (in seconds)
    ramp_duration = ramp_duration
    
    # Set the number of repetitions of the protocol
    n_reps = 1
    
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
        
        # Generate a linear ramp back to the start voltage
        voltage_ramp = np.linspace(end_voltage, start_voltage, n_samples)
        # Append the voltage and time data to the lists
        voltage_data += list(voltage_ramp)
        time_data += [dt] * n_samples
    
    # Convert the lists to NumPy arrays
    voltage_data = np.array(voltage_data, dtype=np.double)
    time_data = np.array(time_data)

    if display_protocol is True:
        temporal_position = np.linspace(start=0, stop=(len(voltage_data) / sampling_rate), num=(len(voltage_data)))
        
        fig, axes = plt.subplots()
        axes.plot(temporal_position, voltage_data)
        axes.set (xlabel = 'Time (s)', ylabel ='Voltage (mV)', title = "Voltage Clamp Ramp Protocol")
        axes.spines['top'].set_visible(False)
        axes.spines['right'].set_visible(False)
        
        fig.show
    x = np.arange(len(voltage_data), dtype=int)
    holding_time = np.full_like(x, 1/sampling_rate, dtype=np.double)
    # Combine the voltage and time data into a single NumPy array
    data_full = np.vstack((holding_time, voltage_data)).T
    if save_csv is True:
        np.savetxt("voltage_ramp_%s_to_%s.csv" % (start_voltage,end_voltage),
                   data_full,
                   delimiter=",")
    return voltage_data


# Generate a voltage step protocol
def generate_voltage_steps(sampling_rate=10e3,holding_potential=-70, min_voltage=-80,max_voltage=80,step_size=10,step_duration=0.5,inter_phase_interval=0.1,inter_stimulus_interval=0.25,n_reps=1,display_protocol=False):
    import numpy as np
    import matplotlib.pyplot as plt

    # Define the voltage levels for the intrinsic neuronal property protocol
    voltage_levels = []
    for level_number in range(int((max_voltage-min_voltage) / step_size)+1):
        voltage_levels += [min_voltage + (level_number * step_size)]


    # Create an empty list to store the voltage and time data
    voltage_data = []
    time_data = []

    # Generate the intrinsic neuronal property protocol
    for i in range(n_reps):
        for v in voltage_levels:
            # Calculate the number of samples for the phase duration
            n_samples = int(step_duration * sampling_rate)
            isi_samples = int(inter_stimulus_interval * sampling_rate)
            # Append the voltage and time data to the lists
            voltage_data += [v] * n_samples
            voltage_data += [holding_potential] * isi_samples
            time_data += [step_duration] * n_samples
            time_data += [inter_phase_interval] * isi_samples
        # Calculate the number of samples for the inter-phase interval
        n_samples = int(inter_phase_interval * sampling_rate)
        # Append the voltage and time data to the lists
        voltage_data += [holding_potential] * n_samples
        time_data += [inter_phase_interval] * n_samples

    # Convert the lists to NumPy arrays
    voltage_data = np.array(voltage_data, dtype=np.double)
    time_data = np.array(time_data)

    if display_protocol is True:
        temporal_position = np.linspace(start=0, stop=(len(voltage_data) / sampling_rate), num=(len(voltage_data)))
        fig, axes = plt.subplots()
        axes.plot(temporal_position, voltage_data)
        axes.set (xlabel = 'Time (s)', ylabel ='Voltage (mV)', title = "Voltage Clamp I/V Curve Protocol")
        axes.spines['top'].set_visible(False)
        axes.spines['right'].set_visible(False)
        fig.show
    return voltage_data

# Generate a current step protocol
def generate_current_steps(sampling_rate=10e3,holding_current=0, min_current=-500,max_current=500,step_size=100,step_duration=0.5,inter_phase_interval=0.1,inter_stimulus_interval=0.25,n_reps=1,display_protocol=False):
    import numpy as np
    import matplotlib.pyplot as plt

    
    # Define the current levels for the intrinsic neuronal property protocol
    current_levels = []
    for level_number in range(int((max_current-min_current) / step_size)+1):
        current_levels += [min_current + (level_number * step_size)]
    


    # Create an empty list to store the current and time data
    current_data = []
    time_data = []
    
    # Generate the intrinsic neuronal property protocol
    for i in range(n_reps):
        for v in current_levels:
            # Calculate the number of samples for the phase duration
            n_samples = int(step_duration * sampling_rate)
            isi_samples = int(inter_stimulus_interval * sampling_rate)
            # Append the current and time data to the lists
            current_data += [v] * n_samples
            current_data += [holding_current] * isi_samples
            time_data += [step_duration] * n_samples
            time_data += [inter_phase_interval] * isi_samples
        # Calculate the number of samples for the inter-phase interval
        n_samples = int(inter_phase_interval * sampling_rate)
        # Append the current and time data to the lists
        current_data += [holding_current] * n_samples
        time_data += [inter_phase_interval] * n_samples
        if i < n_reps:
            #interstimulus interval duration
            current_data += [inter_stimulus_interval] * n_samples
            time_data += [inter_stimulus_interval] * n_samples
    # Convert the lists to NumPy arrays
    current_data = np.array(current_data, dtype=np.double)
    time_data = np.array(time_data)
    
    if display_protocol is True:
        temporal_position = np.linspace(start=0, stop=(len(current_data) / sampling_rate), num=(len(current_data)))
        
        fig, axes = plt.subplots()
        axes.plot(temporal_position, current_data)
        axes.set (xlabel = 'Time (s)', ylabel ='current (mV)', title = "current Clamp I/V Curve Protocol")
        axes.spines['top'].set_visible(False)
        axes.spines['right'].set_visible(False)
        fig.show
    return current_data

# Generate a membrane test protocol
def generate_membrane_test(sampling_rate=10e3,holding_potential=-70, min_voltage=-80,max_voltage=-70,step_size=10,step_duration=0.2,inter_phase_interval=0.5,n_reps=10,display_protocol=False):
    import numpy as np
    import matplotlib.pyplot as plt
    
    # Define the voltage levels for the intrinsic neuronal property protocol
    voltage_levels = []
    for level_number in range(int((max_voltage-min_voltage) / step_size)+1):
        voltage_levels += [min_voltage + (level_number * step_size)]

    # Create an empty list to store the voltage data
    voltage_data = []

    # Generate the intrinsic neuronal property protocol
    for i in range(n_reps):
        for v in voltage_levels:
            # Calculate the number of samples for the phase duration
            n_samples = int(step_duration * sampling_rate)
            # Append the voltage and time data to the lists
            voltage_data += [v] * n_samples
        # Calculate the number of samples for the inter-phase interval
        n_samples = int(inter_phase_interval * sampling_rate)

        # Append the voltage and time data to the lists
        voltage_data += [holding_potential] * n_samples

        # Get the enchanced capacitance
        ramp_data = generate_voltage_ramp(start_voltage=-70, end_voltage=-80, ramp_duration=0.1, sampling_rate=10e3, display_protocol=False, save_csv=False)

        # Append the ramp data to the voltage data
        voltage_data += list(ramp_data)
        voltage_data += [holding_potential] * n_samples

    # Convert the lists to NumPy arrays
    voltage_data = np.array(voltage_data, dtype=np.double)

    # Pad the recording with 1 second of holding value
    data = np.concatenate(( np.zeros(int(sampling_rate))+holding_potential, voltage_data, np.zeros(int(sampling_rate))+holding_potential))
    if display_protocol is True:
        temporal_position = np.linspace(start=0, stop=(len(voltage_data) / sampling_rate), num=(len(voltage_data)))
        fig, axes = plt.subplots()
        axes.plot(temporal_position, voltage_data)
        axes.set (xlabel = 'Time (s)', ylabel ='Voltage (mV)', title = "Membrane Test Protocol")
        axes.spines['top'].set_visible(False)
        axes.spines['right'].set_visible(False)
        fig.show

    return data

def pipette_properties(base_voltage=0, base_duration=0.1, pulse_voltage=10, pulse_duration=0.02, n_reps=10):
    """
    Generate a test protocol for measuring pipette properties before patching. This function is special compared to most as each individual point is not necessary for generating a CSV file.

    Parameters
    ----------
    base_voltage : int, optional
        Baseline potential in mV. The default is 0.
    base_duration : float, optional
        Holding duration in ms. The default is 0.01.
    pulse_voltage : int, optional
        Size of voltage pulse. The default is 10.
    pulse_duration : float, optional
        Duration of voltage pulse in ms. The default is 0.02.
    n_reps : int, optional
        Number of voltage pulses to perform. The default is 10.


    Returns
    -------
    None.

    """
    import numpy as np
    import matplotlib.pyplot as plt
    
    # Create list of voltages
    applied_voltage = [base_voltage, pulse_voltage, base_voltage]
    time_data = [base_duration, pulse_duration, base_duration]

    # Convert the lists to NumPy arrays
    applied_voltage = np.array(applied_voltage, dtype=np.double)
    time_data = np.array(time_data)
    
    pipette_test = np.

    return applied_voltage