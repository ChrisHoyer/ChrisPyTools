import numpy as np
   
def EngNot( x , sig_figs=3, si=True, exp=True):
    """
    Format a number in engineering notation using powers of 10 in multiples of 3.
    
    Based on `Stack Overflow <https://stackoverflow.com/questions/17973278/python-decimal-engineering-notation-for-mili-10e-3-and-micro-10e-6>`_.

    
    Parameters
    ----------
    x : float or int
        The numeric value to format. If NaN, returns an empty string.

    sig_figs : int, optional
        Number of significant figures to display (default is 3).

    si : bool, optional
        If True, use SI unit prefixes instead of exponent notation. E.g., "k" for 10³, "n" for 10⁻⁹.
        If False, the format uses exponential notation like "e3" (default is True).

    exp : bool, optional
        Reserved for future use. Currently has no effect on formatting (default is True).

    Returns
    -------
    str
        A string representation of `x` in engineering notation, optionally using SI prefixes.
    """
    
    if np.isnan(x):
        return ""
    
    
    x = float(x)
    sign = ''
    if x < 0:
        x = -x
        sign = '-'
    if x == 0:
        exp = 0
        exp3 = 0
        x3 = 0
    else:
        exp = int(np.floor(np.log10( x )))
        exp3 = exp - ( exp % 3)
        x3 = x / ( 10 ** exp3)
        x3 = round( x3, -int( np.floor(np.log10( x3 )) - (sig_figs-1)) )
        if x3 == int(x3): # prevent from displaying .0
            x3 = int(x3)

    if si and exp3 >= -24 and exp3 <= 24 and exp3 != 0:
        exp3_text = 'yzafpnum kMGTPEZY'[ exp3 // 3 + 8]
    elif exp3 == 0:
        exp3_text = ''
    else:
        exp3_text = 'e%s' % exp3

    return ( '%s%s%s') % ( sign, x3, exp3_text)
  
     
def RevEngNot( x ):
    """
    Convert a string formatted with SI unit prefixes into a float.

    Parameters
    ----------
    x : str
        A numeric string with an optional SI unit prefix. Supported prefixes:
        - Positive: 'k', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y'
        - Negative: 'm', 'u', 'n', 'p', 'f', 'a', 'z', 'y'

    Returns
    -------
    float
        The corresponding numeric value. If the input is invalid or results in NaN, returns an empty string.
    """
    
    pos_postfixes = ['k', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y']
    neg_postfixes = ['m', 'u', 'n', 'p', 'f', 'a', 'z', 'y']

    num_postfix = x[-1]
    
    if num_postfix in pos_postfixes:
        num = float(x[:-1])
        num*=10**((pos_postfixes.index(num_postfix)+1)*3)
    elif num_postfix in neg_postfixes:
        num = float(x[:-1])
        num*=10**(-(neg_postfixes.index(num_postfix)+1)*3)
    else:
        num = float(x)
 
    if np.isnan(num):
        return ""
             
    return num

