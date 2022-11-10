__author__ = "Jakub Franěk"
__email__ = "tofugangsw@gmail.com"

from typing import Union
from sys import _getframe
from os.path import basename, dirname, realpath


################################################################################

ONE_STAR_PREFIX = "\u2605  "
TWO_STARS_PREFIX = "\u2605\u2605 "
PUZZLE_NUM_1 = 1
PUZZLE_NUM_2 = 2
STAR_PREFIXES = {
    PUZZLE_NUM_1: ONE_STAR_PREFIX,
    PUZZLE_NUM_2: TWO_STARS_PREFIX
}


################################################################################

def print_puzzle_solution(solution: Union[str, int]) -> None:
    """
    Prints puzzle solution. Caller information is used to get day and puzzle
    numbers. This works as long as the caller script is saved in a directory
    with the day number being last two characters in its name and the caller
    function having puzzle number (digit 1 or 2) as the last character in its
    name.

    :param solution: puzzle solution
    """

    caller_file_name = _getframe(1).f_code.co_filename
    caller_function_name = _getframe(1).f_code.co_name
    caller_dir_name = basename(dirname(realpath(caller_file_name)))

    puzzle_number = int(caller_function_name[-1])
    day_number = int(caller_dir_name[-2:])

    print("{}DAY {:02d}; puzzle {}: {}".format(
        STAR_PREFIXES[puzzle_number], day_number, puzzle_number, solution))

################################################################################
