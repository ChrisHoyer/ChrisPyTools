"""
This module provides utility functions for numerical formatting and terminal interaction.

Available Functions
-------------------

- EngNot           : Converts numeric values into engineering notation with optional SI prefixes.
- RevEngNot        : Parses strings in engineering notation (e.g., '10k', '2.2u') back to numeric values.
- printProgressBar : Displays a live progress bar in the terminal during loops or iterative processes.

These tools are designed for convenience in scientific computing, logging, and command-line applications.
"""

from .EngNot import EngNot, RevEngNot
from .ProgressBar import printProgressBar

__all__ = [
    'EngNot', 'RevEngNot', 'printProgressBar'
]
