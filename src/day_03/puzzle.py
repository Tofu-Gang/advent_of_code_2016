__author__ = "Jakub Franěk"
__email__ = "tofugangsw@gmail.com"

"""
--- Day 3: Squares With Three Sides ---

Now that you can think clearly, you move deeper into the labyrinth of hallways 
and office furniture that makes up this part of Easter Bunny HQ. This must be a 
graphic design department; the walls are covered in specifications for 
triangles.

Or are they?
"""

from itertools import combinations
from more_itertools import flatten, chunked
from typing import Tuple

INPUT_FILE_PATH = "src/day_03/input.txt"


################################################################################

def _is_triangle(sides: Tuple[int]) -> bool:
    """
    :param sides: three sides of a potential triangle
    :return: True if the three sides can form a triangle, False otherwise
    """

    return all(sum(combination) > sum(set(sides) ^ set(combination))
               for combination in combinations(sides, 2))


################################################################################

def puzzle_01() -> int:
    """
    The design document gives the side lengths of each triangle it describes,
    but... 5 10 25? Some of these aren't triangles. You can't help but mark the
    impossible ones.

    In a valid triangle, the sum of any two sides must be larger than the
    remaining side. For example, the "triangle" given above is impossible,
    because 5 + 10 is not larger than 25.

    In your puzzle input, how many of the listed triangles are possible?

    :return: number of possible triangles
    """

    with open(INPUT_FILE_PATH, "r") as f:
        triangles = tuple(tuple(map(lambda element: int(element), line.split()))
                          for line in f.readlines())
        return len(tuple(filter(_is_triangle, triangles)))


################################################################################

def puzzle_02() -> int:
    """
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

    :return: number of possible triangles
    """

    with open(INPUT_FILE_PATH, "r") as f:
        lines = [tuple(map(lambda element: int(element), line.split()))
                 for line in f.readlines()]
        columns = tuple(flatten(zip(*lines)))
        triangles = tuple(map(lambda triangle: tuple(triangle),
                              chunked(columns, 3)))
        return len(tuple(filter(_is_triangle, triangles)))

################################################################################
