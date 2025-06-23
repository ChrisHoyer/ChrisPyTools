import matplotlib.ticker as tck
from cycler import cycler
import numpy as np

# Black and White Style
monochrome = (cycler('color', ['k']) * cycler('linestyle', ['-', '--', ':']) * cycler('marker', ['^', '.','v', '<', '>']))

#############################################################################
###         Generate Generic Plot
#############################################################################
def BasePlot(func, ax, Plot_list, X_label, Y_label, Legend=True, LegendLoc=0,
             TwinX=None, TwinY=None, TwinReuseTicks="BOTH", Ylim=None, Xlim=None,
             XAutolim=True, fontsize=7, TicksEng=True, XTicksLabel=None,
             YTicksLabel=None, legendcol=1, fontsize_label=8, yaxis_pad=0, xaxis_pad=0, 
             BlackWhite=False, grid=True, minor_gridcolor="#e8e8e8", major_gridcolor="#d0d0d0",
             LegendFrame=True, funcReturn=False, major_gridlw=1.2, minor_gridlw=1.0,
             minor_gridzorder=0, major_gridzorder=0, FlatGridPlot=False,
             **kwargs):
    """
    Prepares a plot using a specified plotting function and applies common layout settings.
    
    Args:
        func (Callable): Plotting function that takes (ax, plot, Y_label, X_label) as input (e.g. LinearPlot)
        ax (matplotlib.axes.Axes): Axis to plot on.
        Plot_list (list): A list of plot elements, e.g. [X, Y, label, optional args].
        X_label (str or tuple): X-axis label, optionally (label, unit, scale).
        Y_label (str or tuple): Y-axis label, optionally (label, unit, scale).

        Legend (bool, optional): Show legend. Defaults to True.
        LegendLoc (int, optional): Location code for legend. Defaults to 0.
        legendcol (int, optional): Number of columns in legend. Defaults to 1.
        LegendFrame (bool, optional): Show a box around the legend. Defaults to True.
        BlackWhite (bool, optional): Enable monochrome color scheme. Defaults to False.
        fontsize (int, optional): Font size for ticks and legend. Defaults to 7.
        fontsize_label (int, optional): Font size for axis labels. Defaults to 8.
        xaxis_pad (int, optional): Padding between X label and axis. Defaults to 0.
        yaxis_pad (int, optional): Padding between Y label and axis. Defaults to 0.
    
        Xlim (tuple, optional): Set X-axis limits. Defaults to None.
        Ylim (tuple, optional): Set Y-axis limits. Defaults to None.
        XAutolim (bool, optional): Automatically calculate X-axis limits. Defaults to True.
    
        TicksEng (bool, optional): Enable engineering tick formatting. Defaults to True.
        XTicksLabel (int, optional): Show every nth X-axis tick. Defaults to None.
        YTicksLabel (int, optional): Show every nth Y-axis tick. Defaults to None.
    
        grid (bool, optional): Enable major/minor grid lines. Defaults to True.
        major_gridcolor (str, optional): Color of major grid lines. Defaults to "#d0d0d0".
        minor_gridcolor (str, optional): Color of minor grid lines. Defaults to "#e8e8e8".
        major_gridlw (float, optional): Line width of major grid. Defaults to 1.2.
        minor_gridlw (float, optional): Line width of minor grid. Defaults to 1.0.
        major_gridzorder (int, optional): Z-order of major grid. Defaults to 0.
        minor_gridzorder (int, optional): Z-order of minor grid. Defaults to 0.
        FlatGridPlot (bool, optional): Force static grid layout. Defaults to False.
    
        TwinX (Axes, optional): Add a second X-axis. Defaults to None.
        TwinY (Axes, optional): Add a second Y-axis. Defaults to None.
        TwinReuseTicks (str, optional): Reuse tick locations ('NONE', 'AX1', 'BOTH'). Defaults to "BOTH".
    
        funcReturn (bool, optional): Return values from plot function. Defaults to False.
        **kwargs: Additional keyword arguments passed to `func`.
    
    Returns:
        matplotlib.axes.Axes or list: Axis object if `funcReturn` is False,
        otherwise a list of return values from `func`.
    """

    # BlackWhite Default Settings
    if BlackWhite:
        ax.set_prop_cycle(monochrome)
        
    # for multiple returns
    returnvals = []
        
    # check if Plot has entries
    if len(Plot_list) == 0:
        print("Nothing to Plot!")
        return
    
    for index in range(len(Plot_list)):
        
        plot = Plot_list[index]
        
        # Call Specific Plotting Function
        if funcReturn:
            ax, x_plot, returnval = func(ax, plot, Y_label, X_label)
            returnvals.append(returnval)
            
        else:
            ax, x_plot = func(ax, plot, Y_label, X_label)
        
    # label
    ax.set_ylabel(Y_label[0], labelpad=yaxis_pad)
    ax.set_xlabel(X_label[0], labelpad=xaxis_pad)
    
    # ticks in engineering formatter
    if TicksEng:
        ax.yaxis.set_major_formatter(tck.EngFormatter(unit=Y_label[1]))
        ax.xaxis.set_major_formatter(tck.EngFormatter(unit=X_label[1]))
    
    # xlimit
    if XAutolim:
        
        # search min and max x values
        x_limit_min = np.min(x_plot)
        x_limit_max = np.max(x_plot)
                       
        # iterate all traces
        for trace in ax.get_lines():
            
            # Length should be more than 2 points
            if len(trace.get_xdata()) > 2:
            
                # find new min value
                if np.min(trace.get_xdata()) < x_limit_min:
                    x_limit_min = np.min(trace.get_xdata())
     
                # find new min value
                if np.max(trace.get_xdata()) > x_limit_max:
                    x_limit_max = np.max(trace.get_xdata())   
        
        # set x limit
        ax.set_xlim([x_limit_min,x_limit_max])

    # xlimit    
    if Xlim:
        ax.set_xlim([Xlim[0],Xlim[1]])
        
    # ylimit    
    if Ylim:
        ax.set_ylim([Ylim[0],Ylim[1]])
        
    # set font sizes (all)
    for item in ([ax.title, ax.xaxis.label, ax.yaxis.label] +
             ax.get_xticklabels() + ax.get_yticklabels()):
        item.set_fontsize(fontsize)
    
    # set font size label
    for item in ([ax.xaxis.label, ax.yaxis.label]):
        item.set_fontsize(fontsize_label)

    # =================================== 
    # change XTick Label Position
    if XTicksLabel:
        
        # change visibility of each Nth tick
        for (index,label) in enumerate(ax.xaxis.get_ticklabels()):
            if index % XTicksLabel != 0:
                label.set_visible(False)

    # change YTick Label Position
    if YTicksLabel:
        
        # change visibility of each Nth tick
        for (index,label) in enumerate(ax.yaxis.get_ticklabels()):
            if index % XTicksLabel != 0:
                label.set_visible(False)                
                
    # ===================================    
    # Legend and grid for two axis
    if not(TwinX==None) and type(TwinX) == type(ax):

        # include axis labels in single legend
        all_lines = TwinX.get_lines() + ax.get_lines()
        all_labels = [l.get_label() for l in all_lines]
        
        if Legend:        
            # plot legend
            TwinX.legend(all_lines, all_labels, loc=LegendLoc) 
        
        # Align Axis
        AlignAxis(ax, TwinX, AxisType="Y", Method=TwinReuseTicks)
        
    elif not(TwinY==None) and type(TwinY) == type(ax):
 
        # include axis labels in single legend
        all_lines = TwinY.get_lines() + ax.get_lines()
        all_labels = [l.get_label() for l in all_lines]

        if Legend:        
            # plot legend
            TwinY.legend(all_lines, all_labels, frameon=LegendFrame, loc=LegendLoc) 
        
        # Align Axis
        AlignAxis(ax, TwinY, AxisType="X", Method=TwinReuseTicks)


    # ===================================    
    # grid and legend
    else:
        
        if Legend:
            # legend
            ax.legend(frameon=LegendFrame, loc=LegendLoc, fontsize=fontsize, ncol=legendcol)
            
        if grid:
            
            if minor_gridlw > 0.0:
                ax.minorticks_on()
                ax.grid(which='minor', color = minor_gridcolor, linestyle=':',
                        linewidth = minor_gridlw, zorder = minor_gridzorder)
                
            ax.grid(which='major', color=major_gridcolor, linestyle='-',
                    linewidth=major_gridlw, zorder = major_gridzorder) 

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
        BasePlot(func, ax, Plot_list, X_label, Y_label, Legend=Legend, LegendLoc=LegendLoc,
                TwinX=TwinX, TwinY=TwinY, TwinReuseTicks=TwinReuseTicks,  Ylim=Ylim, Xlim=Xlim,
                XAutolim=XAutolim, fontsize=fontsize, TicksEng=TicksEng, XTicksLabel=XTicksLabel,
                YTicksLabel=YTicksLabel,legendcol=legendcol,fontsize_label=fontsize_label,
                yaxis_pad=yaxis_pad, xaxis_pad=xaxis_pad, BlackWhite=BlackWhite, 
                minor_gridcolor=minor_gridcolor, major_gridcolor=major_gridcolor,
                LegendFrame=LegendFrame, funcReturn=funcReturn, major_gridlw=major_gridlw, minor_gridlw=minor_gridlw,
                major_gridzorder=major_gridzorder, minor_gridzorder=minor_gridzorder, 
                FlatGridPlot=False, grid = False, **kwargs)


                
        # reset limits
        ax.set_xlim(xlim) 
        ax.set_ylim(ylim)
        
        # hide normal grid
        ax.grid(visible=False, which="both")                      

    #return
    if funcReturn:
        return returnvals
    else:
        return ax

#############################################################################
###         Align two Y-axis
#############################################################################
def AlignAxis(ax1, ax2, AxisType="Y", Method="NONE"):
    """
    Aligns two Matplotlib axes (ax1 and ax2) along either the X or Y axis
    so that their ticks are harmonized.

    This function is useful for twin-axis plots where both sides should share
    tick positions or spacing for visual consistency.

    Args:
        ax1 (matplotlib.axes.Axes): First axis to align.
        ax2 (matplotlib.axes.Axes): Second axis to align.
        AxisType (str, optional): Axis to align — either "Y" or "X". Defaults to "Y".
        Method (str, optional): 
            Tick alignment strategy:
            
            - "NONE": Do not align (no-op).  
            - "AX1": Use ax1’s ticks as reference (not implemented).  
            - "BOTH": Recalculate ticks for both axes symmetrically.  

    Returns:
        None: This function modifies the axes in place.

    Note:
        Only the "BOTH" method is currently implemented. If "NONE" or
        unsupported combinations are selected, the function returns early.
    """

    # Generate new Ticks Function
    def Generate_newTicks(ax_dy, ax_ystart, max_ticks):
        
        # Check Intervall
        ax_intervall = np.ceil(ax_dy/(max_ticks - 1))
        
        # Generate new Intervall
        ax_dy_new = (max_ticks -1) * ax_intervall
        
        # generate new Ticks                
        ax_ticks_new = np.linspace(ax_ystart,
                                   ax_ystart+ax_dy_new,
                                   max_ticks)
        
        return ax_ticks_new

#############################################################################  
        
    # Find Round Digits
    def Generate_RoundPoint(ax_dy, max_ticks):
        
        # Check Decimal
        log = np.log10(abs(ax_dy/max_ticks))
        exponent = np.floor(log)-1
        
        # Generate Rounded Value
        ax_roundto = 10**exponent
        
        return ax_roundto
    
#############################################################################  
         
    if Method == "BOTH":
        
        # try to align both axis using 
        if AxisType == "Y":
            # get maximum number of ticks
            max_ticks = max(len(ax1.get_yticks()),len(ax2.get_yticks()))
                
            # get axis distance between ticks
            ax1_dy = ax1.get_ybound()[1] - ax1.get_ybound()[0]   
            ax2_dy = ax2.get_ybound()[1] - ax2.get_ybound()[0]
            
        elif  AxisType == "X":
            # get maximum number of ticks
            max_ticks = max(len(ax1.get_xticks()),len(ax2.get_xticks()))
                
            # get axis distance between ticks
            ax1_dy = ax1.get_xbound()[1] - ax1.get_xbound()[0]   
            ax2_dy = ax2.get_xbound()[1] - ax2.get_xbound()[0]
         
        # Roundto Number
        ax1_roundto = Generate_RoundPoint(ax1_dy, max_ticks)
        ax2_roundto = Generate_RoundPoint(ax2_dy, max_ticks)
    
        
        if AxisType == "Y":     
            # get axis bounds and scale
            YBound_ax1 = [np.floor(ax1.get_ybound()[0]/ax1_roundto),
                          np.ceil(ax1.get_ybound()[1]/ax1_roundto)]
            YBound_ax2 = [np.floor(ax2.get_ybound()[0]/ax2_roundto),
                          np.ceil(ax2.get_ybound()[1]/ax2_roundto)]
    
        elif  AxisType == "X":
            # get axis bounds and scale
            YBound_ax1 = [np.floor(ax1.get_xbound()[0]/ax1_roundto),
                          np.ceil(ax1.get_xbound()[1]/ax1_roundto)]
            YBound_ax2 = [np.floor(ax2.get_xbound()[0]/ax2_roundto),
                          np.ceil(ax2.get_xbound()[1]/ax2_roundto)]  
            
        # get axis scaling and scale
        ax1_dy = YBound_ax1[1] - YBound_ax1[0]   
        ax2_dy = YBound_ax2[1] - YBound_ax2[0]
        
        # define starting points
        ax1_start = YBound_ax1[0]
        ax2_start = YBound_ax2[0]
         
        # Generate new Ticks for axis
        ax1_ticks_new =  Generate_newTicks(ax1_dy, ax1_start, max_ticks)
        ax2_ticks_new =  Generate_newTicks(ax2_dy, ax2_start, max_ticks)
        
        # reverse rescaling
        ax1_ticks_new = ax1_ticks_new*ax1_roundto
        ax2_ticks_new = ax2_ticks_new*ax2_roundto

    else:
        #skip
        return
##############################
        
    if AxisType == "Y":    
        # set ticks
        ax1.set_yticks(ax1_ticks_new)
        ax2.set_yticks(ax2_ticks_new)
            
    elif AxisType == "X":
        # set ticks
        ax1.set_xticks(ax1_ticks_new)
        ax2.set_xticks(ax2_ticks_new)       
  
    # jump back    
    return