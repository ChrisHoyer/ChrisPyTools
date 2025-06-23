import sys
import numpy as np
import matplotlib.pyplot as plt

# If using it with pypi, the following line can be removed
sys.path.insert(1, '../src')
import chrispytools.plot as cpy

data1 = np.random.normal(loc=0, scale=1, size=1000)
data2 = np.random.normal(loc=0.5, scale=2, size=1000) + 2


Y_label = [r'Hits', '']
X_label = [r'Value', '']

# Example 1: Histogram
Data_Histo = [ [data1, data1, "Data"] ]

fig = plt.figure(figsize=(3.5, 2.2), dpi=300)
ax = plt.subplot(111)

cpy.HistogramPlot(ax, Data_Histo, X_label, Y_label, Legend=False)

plt.show()

# Example 2: Histogram
# Dataset 
Data_Box = [[[1, 2], [data1, data2], "Data"] ]

# Labels (customize as needed)
X_label = ["Category", ""]
Y_label = ["Value", ""]

fig = plt.figure(figsize=(3.5, 2.2), dpi=300)
ax = plt.subplot(111)

# Use your BoxPlot function
cpy.BoxPlot(ax, Data_Box, X_label, Y_label)

plt.show()