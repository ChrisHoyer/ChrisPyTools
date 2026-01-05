import sys
import numpy as np
import matplotlib.pyplot as plt

# If using from local source during development
sys.path.insert(1, '../src')
import chrispytools.plot as cplt
import chrispytools.signalprocessing as csig

# Create sample data
x = np.linspace(0, 10, 1000)
y_raw = np.sin(40*x) + 5*np.cos(x)

# Example 1: Moving Average Filter
filter_moving = csig.MovingFilter(x, y_raw, N=40)

# Create plot data
plot_data_moving = [
    [x, y_raw, "Unfiltered", 'linestyle=-, linewidth=.5'],
    [filter_moving["XData"], filter_moving["YData"], "Moving Average"]
    ]



# Create labels with units
x_label = ["Time", "s", 1e-3]  # Label, unit, scaling factor (converts to ms)
y_label = ["Amplitude", "V"]


fig = plt.figure(figsize=(3.5, 2.2), dpi=300)
ax = plt.subplot(111)

cplt.LinearPlot(ax, plot_data_moving, x_label, y_label, LegendLoc=4)

plt.show()

# Example 2: Moving Envelope Filter
filter_envelope = csig.MovingFilter(x, y_raw, FilterType="Envelope")

plot_data_envelope = [
    [x, y_raw, "Unfiltered", 'linestyle=-, linewidth=.5'],
    [filter_envelope["XData_max"], filter_envelope["YData_max"], "Envelope High"],
    [filter_envelope["XData_min"], filter_envelope["YData_min"], "Envelope Low"]
    ]


fig = plt.figure(figsize=(3.5, 2.2), dpi=300)
ax = plt.subplot(111)

cplt.LinearPlot(ax, plot_data_envelope, x_label, y_label, LegendLoc=4)

plt.show()

