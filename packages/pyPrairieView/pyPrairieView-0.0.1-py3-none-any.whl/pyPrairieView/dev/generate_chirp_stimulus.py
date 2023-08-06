def generate_chirp_stimulus(freq_max_hz=10,
                            span_sec=10,
                            rate=10000,
                            holding=-70,
                            amplitude=10,
                            display=False):
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

    Returns:
        data (np.array): A 1xM numpy array of the stimulus
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
        plt.ylabel("mV or pA")
        plt.plot(Xs, data)
        plt.axhline(holding, color='r', alpha=.2, ls='--')
        plt.subplot(212, sharex=ax1)
        plt.ylabel("Frequency (Hz)")
        plt.xlabel("Stimulus Time (seconds)")
        plt.plot(zi, cycle_freqs, '.-')
        plt.tight_layout()
        plt.margins(0.02, .1)
        plt.savefig("sine-sweep.png", dpi=100)
        plt.show()

    # pad on both sides with 1 second of zeros
    data = np.concatenate(
        (np.zeros(rate)+holding, data, np.zeros(rate)+holding))

    return data
