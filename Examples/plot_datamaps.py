import sys
import numpy as np
import matplotlib.pyplot as plt

# If using from local source during development
sys.path.insert(1, '../src')
import chrispytools.plot as cpy

# Create example grid data
x = np.linspace(0, 10, 200)
y = np.linspace(0, 5, 100)
X, Y = np.meshgrid(x, y)

# 2D function with clear valleys (e.g., interference pattern)
Z = np.sin(0.5 * X) * np.cos(2 * Y)

# Plot data for PseudoColorPlot
plot_map = [[X, Y, Z, "2D Function", "cmap=viridis, rasterized=True"]]

# Get Y-position of minimum Z for each X
y_min = y[ np.argmin(Z, axis=0) ]
x_min = x

# Compute minima along axis 1 (X-min for each Y)
x_min2 = x[ np.argmin(Z, axis=1) ]
y_min2 = y

minima_line = [ [x_min, y_min, "Min along Y", "color=red, linewidth=1"],
                [x_min2, y_min2, "Min along X", "color=red, linewidth=1, linestyle=--"]
            ]


# Define labels
x_label = ["X Axis", "", 1]
y_label = ["Y Axis", "", 1]

# Plotting
fig = plt.figure(figsize=(5, 3.5), dpi=300)
ax = plt.subplot(111)

# Pseudocolor background
cpy.PseudoColorPlot(ax, plot_map, x_label, y_label, Legend=False)

# Overlay minima as a red contour-like line
cpy.LinearPlot(ax, minima_line, x_label, y_label)

plt.tight_layout()
plt.show()
