__author__ = "Tofu Gang"
__email__ = "tofugangsw@gmail.com"

from os import getcwd
from os.path import join
from re import compile
from typing import Tuple

"""
--- Day 3: Squares With Three Sides ---

Now that you can think clearly, you move deeper into the labyrinth of hallways 
and office furniture that makes up this part of Easter Bunny HQ. This must be a 
graphic design department; the walls are covered in specifications for 
triangles.

Or are they?
"""

################################################################################

SELF_DIR_NAME = "day_03"
INPUT_TXT_NAME = "input.txt"

################################################################################

def _is_triangle(sides: Tuple[int]) -> bool:
    """
    :param sides: three sides of a potential triangle
    :return: True if the three sides can form a triangle, False otherwise
    """

    return sides[0] + sides[1] > sides[2] \
           and sides[0] + sides[2] > sides[1] \
           and sides[1] + sides[2] > sides[0]

################################################################################

def puzzle_1() -> None:
    """
    --- Part One ---

    The design document gives the side lengths of each triangle it describes,
    but... 5 10 25? Some of these aren't triangles. You can't help but mark the
    impossible ones.

    In a valid triangle, the sum of any two sides must be larger than the
    remaining side. For example, the "triangle" given above is impossible,
    because 5 + 10 is not larger than 25.

    In your puzzle input, how many of the listed triangles are possible?
    """

    with open(join(getcwd(), SELF_DIR_NAME, INPUT_TXT_NAME), "r") as f:
        pattern = compile(r'\d+')
        lines = [pattern.findall(line) for line in f.readlines()]
        triangles = [tuple(map(lambda element: int(element), line)) for line in lines]
        # should be 917
        print(len([triangle for triangle in triangles if _is_triangle(triangle)]))

################################################################################

def puzzle_2() -> None:
    """
    --- Part Two ---

    Now that you've helpfully marked up their design documents, it occurs to you
    that triangles are specified in groups of three vertically. Each set of
    three numbers in a column specifies a triangle. Rows are unrelated.

    For example, given the following specification, numbers with the same
    hundreds digit would be part of the same triangle:

    101 301 501
    102 302 502
    103 303 503
    201 401 601
    202 402 602
    203 403 603

    In your puzzle input, and instead reading by columns, how many of the listed
    triangles are possible?
    """

    with open(join(getcwd(), SELF_DIR_NAME, INPUT_TXT_NAME), "r") as f:
        pattern = compile(r'\d+')
        lines = [pattern.findall(line) for line in f.readlines()]
        columns = [int(line[0]) for line in lines] \
                  + [int(line[1]) for line in lines] \
                  + [int(line[2]) for line in lines]
        triangles = [tuple(columns[i:i + 3]) for i in range(0, len(columns), 3)]
        # should be 1649
        print(len([triangle for triangle in triangles if _is_triangle(triangle)]))

################################################################################
