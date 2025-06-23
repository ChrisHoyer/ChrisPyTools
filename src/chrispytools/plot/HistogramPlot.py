from chrispytools.plot.base import BasePlot
import numpy as np

def HistogramPlot(ax, Plot_list, X_label, Y_label, FreedmanDiacoins=True, **kwargs):
    """
    Plots histograms using a standardized plot wrapper.

    This function supports label scaling, user-defined styles, and optionally
    applies the Freedman–Diaconis rule to determine optimal bin widths for the histogram.
    It integrates with :func:`chrispytools.plot.base.BasePlot` for consistent formatting
    and configuration.
        
    Parameters
    ----------
    ax : matplotlib.axes.Axes
        The matplotlib axis object on which to draw the histogram.

    Plot_list : list
        A list of plot entries. Each entry must be a list or tuple of the form:
        ``[XData, YData, Label, style_string (optional)]``

        - **XData** (array-like): Data values to be binned on the X-axis.
        - **YData** (array-like): Typically ignored in histogram plots, but kept for consistency.
        - **Label** (str): Legend label for the histogram trace.
        - **style_string** (str, optional): A comma-separated string of matplotlib style arguments,
          e.g., ``"color=blue,bins=30,alpha=0.6"``.

    X_label : list
        A list of 2 or 3 elements representing the X-axis labeling scheme:
        ``[Label (str), Unit (str), Scale (float, optional)]``

    Y_label : list
        A list of 2 or 3 elements representing the Y-axis labeling scheme:
        ``[Label (str), Unit (str), Scale (float, optional)]``

    FreedmanDiacoins : bool, default=True
        If True, the bin count is automatically computed using the Freedman–Diaconis rule:
        ``bin_width = 2 * IQR * n^(-1/3)``

    **kwargs : dict
        Additional keyword arguments passed to :func:`chrispytools.plot.base.BasePlot`.

    Returns
    -------
    matplotlib.axes.Axes
        The updated axis object containing the histogram.
    """

    def Process_Plot(ax, plot, Y_label, X_label):   
                
        # check dimension of X-Axis if whole trace
        x_plot = plot[0]
        
        # only one marker?
        if np.size(x_plot) > 1:
            y_plot = plot[1][0 : np.size(x_plot)]
        else:
            y_plot = plot[1]
        
        # emtpy argument list
        userargs = {}
                
        # insert plotting arguments
        if len(plot) >= 4:
            args = plot[3].strip().replace(" ", "")
            userargs = dict(e.split('=') for e in args.split(','))
            
        # Check if userargs have only numberic values
        for userarg in userargs:
            
            # check if is int            
            if userargs[userarg].isdigit():
                userargs[userarg] = int(userargs[userarg])
                continue
                
            # check if is float
            if userargs[userarg].replace('.','',1).isdigit():
                userargs[userarg] = float(userargs[userarg])
                continue

        # calulate bins using Freedman–Diaconis_rule
        if FreedmanDiacoins:
            q25, q75 = np.percentile(y_plot, [0.25, 0.75])
            bin_width = 2 * (q75 - q25) * len(y_plot) ** (-1/3)
            userargs["bins"] = round((max(y_plot) - min(y_plot)) / bin_width)
                
        # rescaling of the y-axis required?
        if len(Y_label) == 3:
            y_plot = [y_data*Y_label[2] for y_data in y_plot]
 
        # rescaling of the x-axis required?
        if len(X_label) == 3:
            x_plot = [x_data*X_label[2] for x_data in x_plot]
            
        ax.hist(x_plot, label=plot[2], **userargs)
        
        return ax, x_plot

    # call function and return
    return BasePlot(Process_Plot, ax, Plot_list, X_label, Y_label, **kwargs)
