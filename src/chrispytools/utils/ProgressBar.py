def printProgressBar( iteration: int, total: int, prefix: str = "Progress",
                       suffix: str = "Complete", decimals: int = 1, length: int = 50,
                       fill: str = "█", print_end: str = "\r" ) -> None:
    """
    Displays a terminal progress bar.

    This function prints a dynamically updating progress bar in the terminal.
    It is typically used inside a loop to visually track progress.

    Parameters
    ----------
    iteration : int
        Current iteration count (e.g., loop index).
    total : int
        Total number of iterations.
    prefix : str, optional
        Text displayed before the progress bar.
    suffix : str, optional
        Text displayed after the progress bar.
    decimals : int, optional
        Number of decimal places to show in the percentage.
    length : int, optional
        Total character width of the progress bar.
    fill : str, optional
        Character used to fill the progress portion of the bar.
    print_end : str, optional
        End character printed after the bar.

    Returns
    -------
    None
        Prints directly to stdout.

    """
    if total <= 0:
        raise ValueError("Total must be a positive integer.")

    percent = f"{100 * (iteration / float(total)):.{decimals}f}"
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)

    print(f"\r{prefix} |{bar}| {percent}% {suffix}", end=print_end)

    if iteration >= total:
        print()

  