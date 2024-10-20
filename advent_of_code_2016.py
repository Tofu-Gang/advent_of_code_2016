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

from unittest import TestCase, main

from src.day_01 import puzzle as day_01
from src.day_02 import puzzle as day_02
from src.day_03 import puzzle as day_03
from src.day_04 import puzzle as day_04
from src.day_05 import puzzle as day_05
from src.day_06 import puzzle as day_06
from src.day_07 import puzzle as day_07
from src.day_08 import puzzle as day_08
from src.day_09 import puzzle as day_09
from src.day_10 import puzzle as day_10


################################################################################

class TestAdventOfCode2016(TestCase):

    def test_advent_of_code_2016(self):
        self.assertEqual(day_01.puzzle_01(), 242)
        self.assertEqual(day_01.puzzle_02(), 150)
        self.assertEqual(day_02.puzzle_01(), "45973")
        self.assertEqual(day_02.puzzle_02(), "27CA4")
        self.assertEqual(day_03.puzzle_01(), 917)
        self.assertEqual(day_03.puzzle_02(), 1649)
        self.assertEqual(day_04.puzzle_01(), 173787)
        self.assertEqual(day_04.puzzle_02(), 548)
        self.assertEqual(day_05.puzzle_01(), "1a3099aa")
        self.assertEqual(day_05.puzzle_02(), "694190cd")
        self.assertEqual(day_06.puzzle_01(), "kqsdmzft")
        self.assertEqual(day_06.puzzle_02(), "tpooccyo")
        self.assertEqual(day_07.puzzle_01(), 115)
        self.assertEqual(day_07.puzzle_02(), 231)
        self.assertEqual(day_08.puzzle_01(), 121)
        # result of day 8 puzzle 2 is ASCII art
        self.assertEqual(day_09.puzzle_01(), 152851)
        self.assertEqual(day_09.puzzle_02(), 11797310782)
        self.assertEqual(day_10.puzzle_01(), 118)
        self.assertEqual(day_10.puzzle_02(), 143153)

################################################################################


if __name__ == '__main__':
    main()

################################################################################
