from chrispytools.plot.base import BasePlot
import numpy as np

def PseudoColorPlot(ax, Plot_list, X_label, Y_label, **kwargs):
    """
    Prepares a pseudo color (pcolor) X-Y plot using a standardized plot wrapper.

    This function handles optional label scaling, user-defined line styles, and passes 
    additional configuration to the :func:`chrispytools.plot.base.BasePlot` backend.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        The matplotlib axis object to render the plot on.

    Plot_list : list
        A list of plot entries, where each entry has the format:
        [XData, YData, Label, style_string (optional)]

        - XData (array-like): Data for the X-axis.
        - YData (array-like): Data for the Y-axis.
        - Label (str): Legend label for the plotted trace.
        - style_string (str, optional): A comma-separated string of matplotlib style arguments,
          e.g., ``"linestyle=--, color=red"``.

    X_label : list
        A 2- or 3-element list representing the X-axis label configuration:
        [Label (str), Unit (str), Scale (float, optional)]

    Y_label : list
        A 2- or 3-element list representing the Y-axis label configuration:
        [Label (str), Unit (str), Scale (float, optional)]

    **kwargs : dict
        Additional keyword arguments forwarded to :func:`chrispytools.plot.base.BasePlot`.

    Returns
    -------
    matplotlib.axes.Axes
        The updated axis object with the semi-logarithmic plot rendered.
    """
    
    def Process_Plot(ax, plot, Y_label, X_label):
              
                
        # check dimension
        x_plot = plot[0]
        y_plot = plot[1]
        z_plot = plot[2]
        
        # emtpy argument list
        userargs = {}
                
        # insert plotting arguments
        if len(plot) >= 4:
            args = plot[4].strip().replace(" ", "")
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
                
        # rescaling of the y-axis required?
        if len(Y_label) == 3:
            y_plot = [y_data*Y_label[2] for y_data in y_plot]
 
        # rescaling of the x-axis required?
        if len(X_label) == 3:
            x_plot = [x_data*X_label[2] for x_data in x_plot]
            
        returnval = ax.pcolor(x_plot, y_plot, z_plot, label=plot[3], **userargs)
        
        return ax, x_plot, returnval

    # get collection from Plot
    return BasePlot(Process_Plot, ax, Plot_list, X_label, Y_label, funcReturn=True, **kwargs)

