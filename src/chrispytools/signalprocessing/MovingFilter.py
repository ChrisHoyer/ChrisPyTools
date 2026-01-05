import numpy as np

def _moving_average( Xdata, Ydata, N=3):
    """
    Compute a simple moving average.
    """
    if N < 1:
        raise ValueError("Window size N must be >= 1")

    kernel = np.ones(N) / N
    y_avg = np.convolve(Ydata, kernel, mode="valid")

    half = (N - 1) // 2
    x_avg = Xdata[half : half + len(y_avg)]

    return {
        "XData": x_avg,
        "YData": y_avg,
    }


def _envelope(Xdata, Ydata, dmin=1, dmax=1, split=False):
    """
    Extract upper and lower envelopes of a signal.
    """
    # local extrema
    lmin = (np.diff(np.sign(np.diff(Ydata))) > 0).nonzero()[0] + 1
    lmax = (np.diff(np.sign(np.diff(Ydata))) < 0).nonzero()[0] + 1

    if split:
        mean_val = np.mean(Ydata)
        lmin = lmin[Ydata[lmin] < mean_val]
        lmax = lmax[Ydata[lmax] > mean_val]

    # chunked extrema selection
    lmin = lmin[
        [i + np.argmin(Ydata[lmin[i : i + dmin]]) for i in range(0, len(lmin), dmin)]
    ]
    lmax = lmax[
        [i + np.argmax(Ydata[lmax[i : i + dmax]]) for i in range(0, len(lmax), dmax)]
    ]

    return {
        "XData_min": Xdata[lmin],
        "YData_min": Ydata[lmin],
        "XData_max": Xdata[lmax],
        "YData_max": Ydata[lmax],
    }



def MovingFilter( Xdata, Ydata, FilterType="MovingAvg", **kwargs):

    """
    Applies a simple moving filter to one dimensional data. The filter behavior
    is selected via the ``FilterType`` argument, while filter-specific parameters
    are passed through ``**kwargs``.

    Moving average based on `Moving average or running mean <https://stackoverflow.com/questions/13728392/moving-average-or-running-mean>`_.
    Envelope extraction based on `How to get high and low envelope of a signal <https://stackoverflow.com/questions/34235530/how-to-get-high-and-low-envelope-of-a-signal>`_.
    
    Parameters
    ----------
    Xdata : array-like
        X-axis data corresponding to the input signal.
    
    Ydata : array-like
        Y-axis signal data to be filtered.
    
    FilterType : str, optional
        Selects the filter algorithm to apply.
    
        Supported values are:
    
        - ``"MovingAvg"`` : Simple moving average filter.
        - ``"Envelope"``  : Upper and lower envelope extraction.
    
    **kwargs : dict
        Additional keyword arguments forwarded to the selected filter.
    
        **MovingAvg**
            N : int, optional
                Window size of the moving average (default: ``3``).
    
        **Envelope**
            dmin : int, optional
                Chunk size used to determine local minima (default: ``1``).
            dmax : int, optional
                Chunk size used to determine local maxima (default: ``1``).
            split : bool, optional
                If ``True``, splits the signal by its mean before envelope
                extraction (default: ``False``).
    
    Returns
    -------
    dict
        Dictionary containing the filtered data as NumPy arrays.
    
        **MovingAvg**
            - ``"XData"`` : Filtered X-axis data
            - ``"YData"`` : Smoothed Y-axis data
    
        **Envelope**
            - ``"XData_min"``, ``"YData_min"`` : Lower envelope
            - ``"XData_max"``, ``"YData_max"`` : Upper envelope
    """

    
    Xdata = np.asarray(Xdata)
    Ydata = np.asarray(Ydata)

    if FilterType == "MovingAvg":
        return _moving_average(Xdata, Ydata, **kwargs)

    if FilterType == "Envelope":
        return _envelope(Xdata, Ydata, **kwargs)

    raise ValueError(f"Unknown FilterType: {FilterType!r}")
