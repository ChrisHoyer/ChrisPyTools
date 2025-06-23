from chrispytools.plot.base import BasePlot

def BarPlot(ax, Plot_list, X_label, Y_label, **kwargs):
    """
    Plots a standard bar chart using a consistent plotting interface.

    This function wraps a bar chart with rescaling support, custom styles,
    and optional legend control using :func:`chrispytools.plot.base.BasePlot`.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        The matplotlib axis object to render the plot on.

    Plot_list : list
        A list of plot definitions. Each plot should be a list or tuple with the form:
        ``[XData, YData, Label, style_string (optional)]``

        - **XData** (array-like): Bar positions on the X-axis.
        - **YData** (array-like): Heights of the bars.
        - **Label** (str): Legend label for the bars.
        - **style_string** (str, optional): A comma-separated string of matplotlib style parameters,
          e.g., ``"color=green,width=0.5,align=center"``.

    X_label : list
        A 2- or 3-element list defining the X-axis label and unit:
        ``[Label (str), Unit (str), Scale (float, optional)]``

    Y_label : list
        A 2- or 3-element list defining the Y-axis label and unit:
        ``[Label (str), Unit (str), Scale (float, optional)]``

    **kwargs : dict
        Additional keyword arguments passed to :func:`chrispytools.plot.base.BasePlot`.

    Returns
    -------
    matplotlib.axes.Axes
        The updated axis object with the bar chart rendered.
    """

    def Process_Plot(ax, plot, Y_label, X_label):
           
                
        # check dimension of X-Axis if whole trace
        x_plot = plot[0]
        height_plot = plot[1]
                
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
            
            # check if us bool
            if userargs[userarg] == "True":
                userargs[userarg] = True
                continue            
            if userargs[userarg] == "False":
                userargs[userarg] = False
                continue     
                 
        # rescaling of the x-axis required?
        if len(Y_label) == 3:
            height_plot = height_plot * Y_label[2]
            
        ax.bar(x_plot, height_plot, label=plot[2], **userargs)
        
        return ax, x_plot

    # call function and return
    return BasePlot(Process_Plot, ax, Plot_list, X_label, Y_label, **kwargs)
