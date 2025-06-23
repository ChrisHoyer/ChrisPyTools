import sys
import numpy as np
import matplotlib.pyplot as plt

# If using it with pypi, the following line can be removed
sys.path.insert(1, '../src')
import chrispytools.plot as cpy

# Create sample data
x = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = np.cos(x)
y3 = np.sin(x) * np.cos(x)


# Create plot data
# [ [ X-Data, Y-Data, Label, kwargs for matplotlib ] ]
plot_data = [
    [x, y1, "sin(x)"],
    [x, y2, "cos(x)", 'linestyle=dashed,color=red'],
    [x, y3, "sin(x)*cos(x)", 'linestyle=:,color=green,marker=o,markersize=2']
]

plot_data2 = [ [x, y1, "sin(x)"] ]

# Create labels with units
x_label = ["Time", "s", 1e-3]  # Label, unit, scaling factor (converts to ms)
y_label = ["Amplitude", "V"]

# Example 1: LinearPlot
fig = plt.figure(figsize=(3.5, 2.2), dpi=300)
ax = plt.subplot(111)

cpy.LinearPlot(ax, plot_data, x_label, y_label)

plt.show()

# Example 2: SemiLogXPlot
fig = plt.figure(figsize=(3.5, 2.2), dpi=300)
ax = plt.subplot(111)

cpy.SemiLogXPlot(ax, plot_data, x_label, y_label)

plt.show()

# Example 3: SemiLogYPlot
fig = plt.figure(figsize=(3.5, 2.2), dpi=300)
ax = plt.subplot(111)

cpy.SemiLogYPlot(ax, plot_data, x_label, y_label)

plt.show()

# Example 4: Complex Plot
fig = plt.figure(figsize=(3.5, 2.2), dpi=300)
ax = plt.subplot(111)

cpy.LinearPlot(ax, plot_data2, x_label, y_label)

# Adding a horizontal and vertical lines
cpy.HLinePlot(ax, 0.75, "750 mV", xDistance=0.5, color="C2", lw=1, fontsize=7)
cpy.VLinePlot(ax, 2e-3, "2 ms", yDistance=0.25, color="C1", lw=1, fontsize=7)

# Adding a rectangle to highlight some area
cpy.RectanglePlot(ax, 5e-3, 3e-3, 0, 0.75, color="darksalmon")

plt.show()

