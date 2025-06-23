import numpy as np
import matplotlib.patches as patches

def FillPlot(ax, XAxis, YAxis1, YAxis2=None, XLimits=None, StickyLimits=True,
              minor_gridcolor="#e8e8e8", major_gridcolor="#d0d0d0", 
              major_gridlw=1.2, minor_gridlw=1.0, minor_gridzorder=0, major_gridzorder=0, 
              FlatGridPlot=False, **kwargs):
    """
    Fills the area between two curves or between a curve and baseline on the given axis.
    Optionally applies a custom flat grid overlay with major and minor grid lines.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        The axis to draw on.
    XAxis : array-like
        X-axis data points.
    YAxis1 : array-like
        Y-axis data points for the first curve.
    YAxis2 : array-like or None, optional
        Y-axis data points for the second curve. If None, defaults to zero line (default).
    XLimits : list or tuple of two floats, optional
        Range [start, end] on X-axis to limit the fill area (default is None, use all).
    StickyLimits : bool, optional
        If True, keeps the original axis limits after plotting (default is True).
    minor_gridcolor : str, optional
        Color for minor grid lines (default "#e8e8e8").
    major_gridcolor : str, optional
        Color for major grid lines (default "#d0d0d0").
    major_gridlw : float, optional
        Line width for major grid lines (default 1.2).
    minor_gridlw : float, optional
        Line width for minor grid lines (default 1.0).
    minor_gridzorder : int, optional
        Z-order for minor grid lines (default 0).
    major_gridzorder : int, optional
        Z-order for major grid lines (default 0).
    FlatGridPlot : bool, optional
        If True, draws a custom flat grid by manually plotting grid lines (default False).
    **kwargs
        Additional keyword arguments passed to `ax.fill_between()`.

    Returns
    -------
    None
        Modifies the axis in-place.
    """

    # get old limits
    old_xlim = ax.get_xlim()
    old_ylim = ax.get_ylim()
    
    # limits for x axis
    if XLimits is not None:
        Xstart = np.argmin(np.abs(XAxis - XLimits[0]))
        Xstop = np.argmin(np.abs(XAxis - XLimits[1]))
        
        XAxis = XAxis[Xstart:Xstop]
        YAxis1 = YAxis1[Xstart:Xstop]
        
        if YAxis2 is not None:
            YAxis2 = YAxis2[Xstart:Xstop]
        
        
    if YAxis2 is None:
        YAxis2 = np.zeros(len(YAxis1))

    # generate Fill Pattern         
    ax.fill_between(XAxis, YAxis1, YAxis2,  **kwargs)

    # set old limits
    if StickyLimits:
        ax.set_xlim(old_xlim)
        ax.set_ylim(old_ylim)
        
    # ===================================   
    if FlatGridPlot:
        
        print("!! BETA FUNCTION 'FlatGridPlot' ENABLED! RECURSIVE CALLING OF MAIN FUNCTION !!")
        
        # Obtain X and Y major tick values
        xticks_major = ax.get_xticks()
        yticks_major = ax.get_yticks()

        # Obtain X and Y minor tick values
        xticks_minor = ax.get_xticks(minor = True)
        yticks_minor = ax.get_yticks(minor = True)

        # Obtain limits of the plot
        xlim = ax.get_xlim()
        ylim = ax.get_ylim()
        
        # clear axis to prevent double plotting
        ax.cla()

        # Plot major grid lines
        for xtick in xticks_major:
            ax.plot([xtick, xtick], ylim, color=major_gridcolor, linestyle='-',
                    linewidth=major_gridlw, zorder = major_gridzorder)

        for ytick in yticks_major:
            ax.plot(xlim, [ytick, ytick], color=major_gridcolor, linestyle='-',
                    linewidth=major_gridlw, zorder = major_gridzorder)
            
        # Plot minor grid lines
        if minor_gridlw > 0.0:
            for xtick in xticks_minor:
                ax.plot([xtick, xtick], ylim, color=minor_gridcolor, linestyle=':',
                        linewidth=minor_gridlw, zorder = minor_gridzorder)
            
            for ytick in yticks_minor:
                ax.plot(xlim, [ytick, ytick], color=minor_gridcolor, linestyle=':',
                        linewidth=minor_gridlw, zorder = minor_gridzorder)
                
        # recall function for plotting the content without grid generation
        FillPlot(ax, XAxis, YAxis1, YAxis2 = YAxis2, XLimits = XLimits,
                 StickyLimits = StickyLimits, minor_gridcolor = minor_gridcolor,
                 major_gridcolor = major_gridcolor, major_gridlw = major_gridlw,
                 minor_gridlw = minor_gridlw, minor_gridzorder = minor_gridzorder,
                 major_gridzorder = major_gridzorder, FlatGridPlot = False, **kwargs)
        
        # reset limits
        ax.set_xlim(xlim) 
        ax.set_ylim(ylim)
        
        # hide normal grid
        ax.grid(visible=False, which="both")  


def RectanglePlot(ax, xCenter, xSpan, yCenter, ySpan,
                   fullSpanY=False, StickyLimits=True, **kwargs):
    """
    Draws a rectangle patch centered at (xCenter, yCenter) with given width and height.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        The axis to draw on.
    xCenter : float
        X-coordinate of the rectangle center.
    xSpan : float
        Width of the rectangle.
    yCenter : float
        Y-coordinate of the rectangle center.
    ySpan : float
        Height of the rectangle.
    fullSpanY : bool, optional
        If True, rectangle spans full current y-axis limits ignoring yCenter and ySpan (default False).
    StickyLimits : bool, optional
        If True, keeps the original axis limits after plotting (default True).
    **kwargs
        Additional keyword arguments passed to `matplotlib.patches.Rectangle()`.

    Returns
    -------
    None
        Modifies the axis in-place.
    """

    # get old limits
    old_xlim = ax.get_xlim()
    old_ylim = ax.get_ylim()
    
    # calculate startpoints
    xstart = xCenter - xSpan/2
    ystart = yCenter - ySpan/2
        
    if fullSpanY:
        ystart = min(old_ylim)
        ySpan = old_ylim[1] - old_ylim[0]

    # generate Rectangle
    rect = patches.Rectangle((xstart,ystart),xSpan, ySpan, **kwargs)          
    ax.add_patch(rect) 

    # set old limits
    if StickyLimits:
        ax.set_xlim(old_xlim)
        ax.set_ylim(old_ylim)
