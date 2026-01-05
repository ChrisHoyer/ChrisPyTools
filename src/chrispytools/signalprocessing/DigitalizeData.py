import numpy as np
import matplotlib.pyplot as plt


def Digitalize_Data( data, clock, chipselect=[], edge_trigger="rising", 
                    high_val=1, low_val=0, trigger_val=0.5, threshold_high=2, threshold_low=0.8,
                    onlyDigi=False, debug=False, muteWarnings=True ):
    """
    Convert analog data streams into a digital bit stream using clock edge sampling.

    The function applies a Schmitt-trigger based digitization to the input signals
    and samples the digital data at specified clock edges. Optionally, sampling
    can be restricted to active chip-select windows.

    Parameters
    ----------
    data : array_like
        Analog data signal to be digitized and sampled.
    clock : array_like
        Analog clock signal used for edge-triggered sampling.
    chipselect : array_like, optional
        Optional analog chip-select signal. If provided, sampling is only
        performed while chip-select is active. Must have the same length
        as `data`.
    edge_trigger : {'rising', 'falling'}, optional
        Selects whether rising or falling edges of the clock are used
        for sampling.
    high_val : int or float, optional
        Digital value assigned to samples above `threshold_high`.
    low_val : int or float, optional
        Digital value assigned to samples below or equal to `threshold_low`.
    trigger_val : float, optional
        Threshold used for edge detection of clock and chip-select signals.
    threshold_high : float, optional
        Upper Schmitt-trigger threshold for digitization.
    threshold_low : float, optional
        Lower Schmitt-trigger threshold for digitization.
    onlyDigi : bool, optional
        If True, returns only the digitized data stream and conversion error
        indices without performing clocked sampling.
    debug : bool, optional
        If True, returns dictionary with additional details for debugging.
    muteWarnings : bool, optional
        If False, prints warnings for values that cannot be digitized.

    Returns
    -------
    binary_data : ndarray or list of ndarray
        If `chipselect` is not provided, returns a one-dimensional array
        containing the sampled digital data.
        If `chipselect` is provided, returns a list of arrays, one per
        chip-select active window.

    Notes
    -----
    - Digitization is performed using a Schmitt trigger to avoid noise-induced
      oscillations near the switching threshold.
    - Samples that cannot be uniquely digitized are removed from all signals
      before edge detection.
    - Clock and chip-select edges are detected using `trigger_val`.
    """

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def digitize(arr):
        """Schmitt-trigger digitization"""
        arr = np.asarray(arr)
        digital = np.empty_like(arr, dtype=float)
        errors = []

        for i, v in enumerate(arr):
            if v > threshold_high:
                digital[i] = high_val
            elif v <= threshold_low:
                digital[i] = low_val
            else:
                digital[i] = v
                errors.append(i)
                
                if not muteWarnings:
                    print(f"Value {v} at index {i} ignored (not in valid range).")

        return digital, errors

    def edge_mask(signal):
        """Return rising or falling edge mask"""
        if edge_trigger == "rising":
            return (signal[:-1] < trigger_val) & (signal[1:] > trigger_val)
        elif edge_trigger == "falling":
            return (signal[:-1] > trigger_val) & (signal[1:] < trigger_val)
        else:
            raise ValueError("edge_trigger must be 'rising' or 'falling'")

    # ------------------------------------------------------------------
    # Only digitization requested
    if onlyDigi:
        return digitize(data)

    # ------------------------------------------------------------------
    # Digitize inputs
    data_dig, err_data = digitize(data)
    clk_dig, err_clk = digitize(clock)

    CS = len(chipselect) == len(data)
    if CS:
        cs_dig, err_cs = digitize(chipselect)
    else:
        err_cs = []

    # Remove invalid samples
    errors = sorted(set(err_data + err_clk + err_cs))

    data = np.delete(data, errors)
    clock = np.delete(clock, errors)
    data_dig = np.delete(data_dig, errors)
    clk_dig = np.delete(clk_dig, errors)

    if CS:
        cs_dig = np.delete(cs_dig, errors)

    # Clock edge detection
    clk_edges = np.where(edge_mask(clk_dig))[0]

    if not CS:
        binary_data = data_dig[clk_edges]
        
        if debug:
            debug_return = [ { 'data_dig': data_dig,
                            'data': data,
                            'clk_dig': clk_dig,
                            'clk': clock,
                            'clk_edge': clk_edges,
                            'cs_start': 0,
                            'cs_stop': len(data_dig)}
                            ]

            return (binary_data, debug_return)

        return binary_data

    # Chip-select windowed sampling
    cs_rising = np.where(edge_mask(cs_dig))[0]
    cs_falling = np.where( (cs_dig[:-1] > trigger_val) & (cs_dig[1:] < trigger_val) )[0]

    n = min(len(cs_rising), len(cs_falling))
    cs_rising = cs_rising[:n]
    cs_falling = cs_falling[:n]

    binary_data = []
    debug_return = []

    for start, stop in zip(cs_rising, cs_falling):
        clk_in_window = clk_edges[(clk_edges >= start) & (clk_edges < stop)]

        if len(clk_in_window) == 0:
            continue

        binary_data.append(data_dig[clk_in_window])

        if debug:
            debug_return.append( { 'data_dig': data_dig,
                                  'data': data,
                                  'clk_dig': clk_dig,
                                  'clk': clock,
                                  'clk_edge': clk_in_window,
                                  'cs_start': start,
                                  'cs_stop': stop}
                                )
    
    if debug:
            return (binary_data, debug_return)
        
    return binary_data