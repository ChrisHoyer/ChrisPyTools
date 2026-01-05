import sys
import numpy as np
import matplotlib.pyplot as plt

# If using from local source during development
sys.path.insert(1, '../src')
import chrispytools.plot as cplt
import chrispytools.signalprocessing as csig


# time axis
t = np.linspace(0, 1, int(1e3), endpoint=False)

# Clock: square wave
clock = 2.5 * (np.sign(np.sin(2 * np.pi * 20 * t)) + 1) / 2
clock += 0.2 * np.random.randn(len(clock))

# Data: slower square wave with noise
data = 2.5 * (np.sign(np.sin(2 * np.pi * 5 * t)) + 1) / 2
data = np.roll(data, 10)
data += 0.2 * np.random.randn(len(data))

# Chip Select: active for two windows
chipselect = np.zeros_like(t)
chipselect[200:500] = 2.5
chipselect[650:900] = 2.5
chipselect += 0.2 * np.random.randn(len(chipselect))

# Create Plot to see the raw signal
fig = plt.figure(figsize=(4.5, 3.2), dpi=300)
x_label = ["", "s"]
y_label = [".", "V"]

ax1 = plt.subplot(311)
cplt.LinearPlot(ax1, [[t, data, "Data"]], x_label, y_label)

ax1.xaxis.set_ticklabels([])
handles, labels = ax1.get_legend_handles_labels()     
ax1.legend(handles, labels, framealpha=1, columnspacing=0.75, handlelength=2,
           frameon=True, fontsize=7, loc=4)

ax2 = plt.subplot(312)
cplt.LinearPlot(ax2, [[t, clock, "Clock"]], x_label, y_label)

ax2.xaxis.set_ticklabels([])
handles, labels = ax2.get_legend_handles_labels()     
ax2.legend(handles, labels, framealpha=1, columnspacing=0.75, handlelength=2,
           frameon=True, fontsize=7, loc=4)

ax3 = plt.subplot(313)
cplt.LinearPlot(ax3, [[t, chipselect, "CS"]], x_label, y_label, LegendLoc=4)

handles, labels = ax3.get_legend_handles_labels()     
ax3.legend(handles, labels, framealpha=1, columnspacing=0.75, handlelength=2,
           frameon=True, fontsize=7, loc=4)

plt.show()

# Run Digitalize_Data
binary_data, debug_output = csig.Digitalize_Data( data=data, clock=clock,
                                                  edge_trigger="rising",
                                                  chipselect = chipselect,
                                                 threshold_high=1.8, threshold_low=0.7, 
                                                 debug=True, muteWarnings=False )



fig = plt.figure(figsize=(4.5, 3.2), dpi=300)

# Create Plot to see the processed signal
ax1 = plt.subplot(311)
ax2 = plt.subplot(312)

x_label = ["", ""]
y_label = [".", "V"]

for debug in debug_output:
    
    start = debug['cs_start']
    stop = debug['cs_stop']
    
    samples = np.arange(0, len(debug['data']))
    samples_dig = np.arange(start, stop)
    
    norm_data = debug['data_dig'][start:stop] / np.max(debug['data_dig'][start:stop])
    norm_clk = debug['clk_dig'][start:stop] / np.max(debug['clk_dig'][start:stop])
    
    cplt.LinearPlot(ax1, [[samples, debug['data'], "Data (Raw)", "lw=0.25, color=C0"],
                          [samples_dig, norm_data, "Data (Dig)", "color=C1"],
                          [debug['clk_edge'], debug['data'][debug['clk_edge']], "Sampled Data", "lw=0, marker=x, markersize=5, color=red"]],
                    x_label, y_label, Legend = False)

    cplt.LinearPlot(ax2, [[samples, debug['clk'], "Clk (Raw)", "lw=0.25, color=C0"],
                          [samples_dig, norm_clk, "Clk (Dig)", "color=C1"]],
                    x_label, y_label, Legend = False)

ax1.xaxis.set_ticklabels([])
handles, labels = ax1.get_legend_handles_labels()     
ax1.legend(handles[0:3], labels[0:3], framealpha=1, columnspacing=0.75, handlelength=2,
           frameon=False, fontsize=7, ncols=3, loc=4, bbox_to_anchor=(0.9, 1))

plt.show()