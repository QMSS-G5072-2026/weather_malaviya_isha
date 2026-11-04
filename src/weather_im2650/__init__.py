# read version from installed package
from importlib.metadata import version
__version__ = version("weather_im2650")

from .weather_im2650 import celsius_to_fahrenheit, summarize_temperatures, clean_readings

__all__ = ["celsius_to_fahrenheit", "summarize_temperatures", "clean_readings"]
