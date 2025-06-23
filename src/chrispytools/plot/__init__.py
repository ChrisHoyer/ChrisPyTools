"""
This module provides a collection of reusable plotting functions with consistent
styling, scaling, and formatting behavior. Each function wraps around a base plotting
interface to simplify usage and unify customization via keyword arguments.

Available Plot Types:

- BarHPlot           : Horizontal bar plot for categorical or binned data.
- BarPlot            : Vertical bar plot for categorical or binned data.
- BoxPlot            : Statistical box plot for visualizing distributions.
- HistogramPlot      : Histogram for visualizing frequency distributions.
- LinearPlot         : Standard linear X-Y plot.
- PseudoColorPlot    : Heatmap-like pseudocolor mesh plotting.
- SemiLogXPlot       : Semi-logarithmic plot with logarithmic scaling on the X-axis.
- SemiLogYPlot       : Semi-logarithmic plot with logarithmic scaling on the Y-axis.

Available Accessories:

- VLinePlot          : Draws a vertical line with an optional label at a specified X position.
- HLinePlot          : Draws a horizontal line with an optional label at a specified Y position.
- FillPlot           : Creates a filled area between two curves or between a curve and zero.
- RectanglePlot      : Adds a rectangular patch to the plot at a specified center and span.

All functions accept a list of plot definitions and standardized axis label formatting.
"""

from .BarHPlot import BarHPlot
from .BarPlot import BarPlot
from .BoxPlot import BoxPlot
from .HistogramPlot import HistogramPlot
from .LinearPlot import LinearPlot
from .PseudoColorPlot import PseudoColorPlot
from .SemiLogXPlot import SemiLogXPlot
from .SemiLogYPlot import SemiLogYPlot
from .LinePlot import VLinePlot, HLinePlot
from .FillPlot import FillPlot, RectanglePlot

__all__ = [
    'BarHPlot', 'BarPlot', 'BoxPlot', 'HistogramPlot',
    'LinearPlot', 'PseudoColorPlot', 'SemiLogXPlot', 'SemiLogYPlot',
    'VLinePlot', 'HLinePlot', 'FillPlot', 'RectanglePlot'
]
