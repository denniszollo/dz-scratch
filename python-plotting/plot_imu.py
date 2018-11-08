import pandas as pd
from bokeh.plotting import figure, output_file, show
from bokeh.layouts import column
from bokeh.models import Range1d
import sys
import numpy as np
import scipy.signal as sig

def fft(data, sample_period, power=False, use_db=False):
    dt = sample_period
    sp = np.fft.rfft(data)
    if power:
        spectrum = (np.abs(sp) * 2 * dt) ** 2
    else: 
        spectrum = np.abs(sp) * 2 * dt
        
    if use_db:
        max_input = np.max(data)
        if power:
            spectrum = 20 * np.log10(spectrum / max_input)
        else:
            spectrum = 10 * np.log10(spectrum / max_input)
    n = len(data)
    freqs = np.fft.fftfreq(n, sample_period)
    
    # Ignore the negative part of frequency. It's because of symmetry of FFT.
    idx = np.argsort(freqs)
    idx = filter(lambda i: freqs[i] > 0, idx)
    
    return freqs[idx], spectrum[idx].real


df = pd.read_csv(sys.argv[1])
output_file(sys.argv[1] + ".html")
plots = []
T = df['GPS TOW [s]'].diff().mode().iloc[0]
print T
for each in df.columns[2:]:
    not_nan = np.logical_not(np.isnan(df[each]))
    vec = df[each][not_nan]
    if len(vec) > 0:
        p = figure(plot_width=800, plot_height=400)
        p.line(df['GPS TOW [s]'][not_nan], vec)
        p.title.text = each
        p.xaxis.axis_label = 'GPS TOW [s]'
        p.yaxis.axis_label = 'Gs'
        plots.append(p)
        p2 = figure(plot_width=800, plot_height=400, y_axis_type="log")
        #freqs, spectrum = fft(vec, 0.01, power=True)
        freqs, power = sig.welch(vec, 1/T)
        print(freqs)
        p2.line(freqs, power)
        p2.xaxis.axis_label = 'Freq [Hz]'
        p2.yaxis.axis_label = 'PSD [V**2/Hz]'
        p2.y_range = Range1d(1e-6, 10)
        plots.append(p2)
show(column(plots))

