"""
This module provides a collection of reusable singal processing functions.

Available Functions:

- MovingFilter       : moving filter with different properties
- Digitalize_Data    : extracts binary data from measured signals (e.g. SPI or I2C)

"""

from .MovingFilter import MovingFilter
from .DigitalizeData import Digitalize_Data

__all__ = [
    'MovingFilter', 'Digitalize_Data'
]
