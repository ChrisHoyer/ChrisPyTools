import numpy as np

def VLinePlot(ax, xValue, xLabel, yDistance=0.5, yPos='up', color='r',
              fontsize=6, horizontalalignment='center', **kwargs):
    """
    Draws a vertical line at a specified x-value on the given axis, with an optional label.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        The axis to draw the vertical line on.
    xValue : float
        The x-coordinate where the vertical line will be drawn.
    xLabel : str
        The text label displayed near the vertical line.
    yDistance : float, optional
        Distance multiplier for label positioning relative to the axis ticks (default is 0.5).
    yPos : {'up', 'down', 'center'}, optional
        Positioning of the label relative to the vertical line:
        - 'up': above the axis upper limit (default)
        - 'down': below the axis lower limit
        - 'center': centered vertically on the axis
    color : str, optional
        Color of the line and label text (default is 'r' for red).
    fontsize : int, optional
        Font size of the label text (default is 6).
    horizontalalignment : str, optional
        Horizontal alignment of the label text (default is 'center').
    **kwargs : dict
        Additional keyword arguments passed to `ax.axvline()`.

    Returns
    -------
    None
    """
    # Add vertical line
    ax.axvline(x=xValue, color=color, **kwargs)

    # find y Position
    ylimits = ax.get_ylim()
    ydistance = np.mean(np.ediff1d(ax.get_yticks())) * yDistance    
    
    # up or down?
    if yPos == 'up':
        ylimits = ylimits[1]
        ydistance = abs(ydistance)
    elif yPos == 'down':
        ylimits = ylimits[0]
        ydistance = -abs(ydistance)
    elif yPos == 'center': 
        ylimits = (ylimits[1] - ylimits[0]) / 2 + ylimits[0]

    # generate Text            
    ax.text(xValue, ylimits + ydistance, xLabel, color=color,
            fontsize=fontsize, horizontalalignment=horizontalalignment)  


def HLinePlot(ax, yValue, yLabel, xDistance=0.4, yDistance=0, xPos='right',
              fontsize=6, verticalalignment='center', color='r',
              TextBG="", TextBG_Pad=1.25, **kwargs):
    """
    Draws a horizontal line at a specified y-value on the given axis, with an optional label.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        The axis to draw the horizontal line on.
    yValue : float
        The y-coordinate where the horizontal line will be drawn.
    yLabel : str
        The text label displayed near the horizontal line.
    xDistance : float, optional
        Distance multiplier for label positioning relative to the axis ticks (default is 0.4).
    yDistance : float, optional
        Vertical offset for the label positioning relative to the horizontal line (default is 0).
    xPos : {'left', 'right', 'center'}, optional
        Positioning of the label relative to the horizontal line:
        - 'right': right side of the axis (default)
        - 'left': left side of the axis
        - 'center': centered horizontally on the axis
    fontsize : int, optional
        Font size of the label text (default is 6).
    verticalalignment : str, optional
        Vertical alignment of the label text (default is 'center').
    color : str, optional
        Color of the line and label text (default is 'r' for red).
    TextBG : str, optional
        Background color for the label text box. If empty, no background is applied.
    TextBG_Pad : float, optional
        Padding for the text background box (default is 1.25).
    **kwargs : dict
        Additional keyword arguments passed to `ax.axhline()`.

    Returns
    -------
    None
    """
    # Add horizontal line
    ax.axhline(y=yValue, color=color, **kwargs)
    yValueLabel = yValue + yDistance

    # find x Position
    xlimits = ax.get_xlim()
    xdistance = np.mean(np.ediff1d(ax.get_xticks())) * xDistance    
    
    # left, right or center?
    if xPos == 'right':
        xlimits = xlimits[1]
        xdistance = abs(xdistance)
    elif xPos == 'left':
        xlimits = xlimits[0]
        xdistance = -abs(xdistance)
    elif xPos == 'center': 
        xlimits = (xlimits[1] - xlimits[0]) / 2 + xlimits[0]
         
    # generate Text            
    t = ax.text(xlimits + xdistance, yValueLabel, yLabel, color=color,
                fontsize=fontsize, verticalalignment=verticalalignment,
                horizontalalignment="center") 
     
    if TextBG:
        t.set_bbox(dict(facecolor=TextBG, linewidth=0, pad=TextBG_Pad))
