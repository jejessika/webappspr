def ma(y, n):
    import numpy as np
    from scipy import signal
    b = np.repeat(1.0 / n, n) # Create impulse response
    yf = signal.lfilter(b, 1, y)  # Filter the signal
    for x in range(n):
        yf[x] = y[x]
    return (yf)