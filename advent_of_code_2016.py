__author__ = "Jakub Franěk"
__email__ = "tofugangsw@gmail.com"

"""
Santa's sleigh uses a very high-precision clock to guide its movements, and the 
clock's oscillator is regulated by stars. Unfortunately, the stars have been 
stolen... by the Easter Bunny. To save Christmas, Santa needs you to retrieve 
all fifty stars by December 25th.

Collect stars by solving puzzles. Two puzzles will be made available on each day 
in the Advent calendar; the second puzzle is unlocked when you complete the 
first. Each puzzle grants one star. Good luck!
"""

from src.day_02 import puzzle

################################################################################

if __name__ == "__main__":
    """
    Runs specified puzzles.
    """

    puzzle.puzzle_01()
    puzzle.puzzle_02()

################################################################################
