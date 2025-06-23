from chrispytools.plot.base import BasePlot
import numpy as np

def BoxPlot(ax, Plot_list, X_label, Y_label, **kwargs):
    """
    Prepares a box plot using a standardized plot wrapper.

    This function supports label scaling, user-defined styles via a string parser,
    and integrates with the :func:`chrispytools.plot.base.BasePlot` backend.

    It calculates automatic box widths if none are provided, and handles
    consistent color formatting for all box components. The legend is automatically
    constructed for each trace based on its label.
    
    Parameters
    ----------
    ax : matplotlib.axes.Axes
        The matplotlib axis object to render the plot on.

    Plot_list : list
        A list of plot entries. Each entry must be a list or tuple of the form:
        ``[XData, YData, Label, style_string (optional)]``

        - **XData** (array-like): Positions on the X-axis for each box.
        - **YData** (list of array-like): Box data for each X point.
        - **Label** (str): Legend label for the box group.
        - **style_string** (str, optional): Comma-separated string of box style arguments
          such as ``"color=blue,widths=0.5"``.

    X_label : list
        A list of 2 or 3 elements for labeling the X-axis:
        ``[Label (str), Unit (str), Scale (float, optional)]``

    Y_label : list
        A list of 2 or 3 elements for labeling the Y-axis:
        ``[Label (str), Unit (str), Scale (float, optional)]``

    **kwargs : dict
        Additional keyword arguments passed to :func:`chrispytools.plot.base.BasePlot`.

    Returns
    -------
    matplotlib.axes.Axes
        The axis object with the rendered box plots.
    """

    def Process_Plot(ax, plot, Y_label, X_label):    
                
        # check dimension
        x_plot = plot[0]
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
            
                
        # rescaling of the y-axis required?
        if len(Y_label) == 3:
            y_plot = [np.asarray(y_data)*Y_label[2] for y_data in y_plot]
 
        # rescaling of the x-axis required?
        if len(X_label) == 3:
            x_plot = [np.asarray(x_data)*X_label[2] for x_data in x_plot]
            
            
        # Color? -> Some Special Threatment
        if "color" in userargs:
            
            color = userargs["color"]
                        
            # patch artist
            userargs["patch_artist"] = True
            userargs["boxprops"] = dict(facecolor=color, color=color, alpha=0.75)
            userargs["capprops"] = dict(color=color)
            userargs["whiskerprops"] = dict(color=color)
            userargs["medianprops"] = dict(color='k')
            userargs["flierprops"] = dict(marker='x', markersize = 2, markeredgecolor=color)
            
            # remove "color" from list
            userargs.pop("color")
            
        # Box Widths
        if not("widths" in userargs):
            
            # calculate box width with 25% of min distance between X Points
            userargs["widths"] = np.mean( np.abs(x_plot-np.roll(x_plot,1)) ) * 0.25
                        
        returnval = ax.boxplot(y_plot, positions=x_plot, **userargs)
        
        # Add Legend to Axis
        handles, labels = ax.get_legend_handles_labels()
        handles.append(returnval["boxes"][0])
        labels.append(plot[2])
        ax.legend(handles, labels)
        
        return ax, x_plot, returnval

    
    # get collection from Plot
    return BasePlot(Process_Plot, ax, Plot_list, X_label, Y_label,
                        funcReturn=True, XAutolim=False, Legend=False, **kwargs)
