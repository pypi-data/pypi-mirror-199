from art import text2art

my_art = text2art("Ceylon-AI", font='tarty1')  # Notice the space between "SPACE" and "ART"
print(my_art)
my_art = text2art("ceylon.ai", font='fancy144')  # Notice the space between "SPACE" and "ART"
print(my_art)
my_art = text2art("version 0.2.5", font='fancy144')  # Notice the space between "SPACE" and "ART"
print(my_art)

from .ceylon import *

__doc__ = ceylon.__doc__
if hasattr(ceylon, "__all__"):
    __all__ = ceylon.__all__

from .agent import Agent
from .agent_manager import CeylonAI
