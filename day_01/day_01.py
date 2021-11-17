__author__ = "Tofu Gang"
__email__ = "tofugangsw@gmail.com"

from os import getcwd
from os.path import join
from typing import Dict, Union

"""
--- Day 1: No Time for a Taxicab ---

You're airdropped near Easter Bunny Headquarters in a city somewhere. "Near", 
unfortunately, is as close as you can get - the instructions on the Easter Bunny 
Recruiting Document the Elves intercepted start here, and nobody had time to 
work them out further.
"""

################################################################################

SELF_DIR_NAME = "day_01"
INPUT_TXT_NAME = "input.txt"

################################################################################

class Santa(object):
    DIRECTION_NORTH = "N"
    DIRECTION_SOUTH = "S"
    DIRECTION_WEST = "W"
    DIRECTION_EAST = "E"
    TURN_LEFT = "L"
    TURN_RIGHT = "R"

    DIRECTIONS = {
        0: DIRECTION_NORTH,
        1: DIRECTION_EAST,
        2: DIRECTION_SOUTH,
        3: DIRECTION_WEST
    }

    KEY_POS_FROM = "FROM"
    KEY_POS_TO = "TO"
    KEY_POS_X = "X"
    KEY_POS_Y = "Y"

################################################################################

    def __init__(self):
        """
        Santa starts at position [0, 0], facing north. X axis grows towards
        east, Y axis grows towards north.
        """

        super()
        self._direction = 0
        self._pos_x = 0
        self._pos_y = 0
        self._paths = []
        self._headquarters = None

################################################################################

    @property
    def fake_hq_distance(self) -> int:
        """
        :return: shortest (Manhattan) distance to the Easter Bunny HQ in blocks,
        according to the part one of the puzzle
        """

        return abs(self._pos_x) + abs(self._pos_y)

################################################################################

    @property
    def real_hq_distance(self) -> int:
        """
        :return: shortest (Manhattan) distance to the Easter Bunny HQ in blocks,
        according to the part two of the puzzle
        """

        return abs(self._headquarters[self.KEY_POS_X]) \
               + abs(self._headquarters[self.KEY_POS_Y])

################################################################################

    def follow_instruction(self, instruction: str) -> None:
        """
        Follow the provided sequence: either turn left (L) or right (R)
        90 degrees, then walk forward the given number of blocks, ending at a
        new intersection.

        :param instruction: one instruction from the Easter Bunny Recruiting
        Document the Elves intercepted
        """

        turn = instruction[0]
        blocks = int(instruction[1:])

        if turn == self.TURN_LEFT:
            self._direction = (self._direction - 1) % 4
        elif turn == self.TURN_RIGHT:
            self._direction = (self._direction + 1) % 4
        else:
            # shouldn't happen
            raise Exception()

        pos_from = self._position()
        if self.DIRECTIONS[self._direction] == self.DIRECTION_NORTH:
            self._pos_y += blocks
        elif self.DIRECTIONS[self._direction] == self.DIRECTION_EAST:
            self._pos_x += blocks
        elif self.DIRECTIONS[self._direction] == self.DIRECTION_SOUTH:
            self._pos_y -= blocks
        elif self.DIRECTIONS[self._direction] == self.DIRECTION_WEST:
            self._pos_x -= blocks
        else:
            # shouldn't happen
            raise Exception()

        pos_to = self._position()
        new_path = {
            self.KEY_POS_FROM: pos_from,
            self.KEY_POS_TO: pos_to
        }
        intersections = list(
            filter(lambda intersection: intersection is not None,
                   [self._intersection(new_path, path) for path in self._paths]))

        try:
            if self._headquarters is None:
                self._headquarters = intersections[0]
        except IndexError:
            pass
        self._paths.append(new_path)

################################################################################

    def _position(self) -> Dict[str, int]:
        """
        :return: current Santa's position
        """

        return {
            self.KEY_POS_X: self._pos_x,
            self.KEY_POS_Y: self._pos_y
        }

################################################################################

    def _is_path_horizontal(self, path: Dict[str, Dict[str, int]]) -> bool:
        """
        :param path: path which orientation we test
        :return: True if the path is horizontal, False otherwise
        """

        return path[self.KEY_POS_FROM][self.KEY_POS_Y] == path[self.KEY_POS_TO][self.KEY_POS_Y]

################################################################################

    def _intersection(
            self,
            path_1: Dict[str, Dict[str, int]],
            path_2: Dict[str, Dict[str, int]]) -> Union[Dict[str, int], None]:
        """
        :param path_1: one of the paths we look for an intersection with
        :param path_2: the second of the paths we look for an intersection with
        :return: either an intersection point, or None if the paths do not
        intersect
        """

        if self._is_path_horizontal(path_1) and not self._is_path_horizontal(path_2):
            horizontal = path_1
            vertical = path_2
        elif self._is_path_horizontal(path_2) and not self._is_path_horizontal(path_1):
            horizontal = path_2
            vertical = path_1
        else:
            # both path are either horizontal or vertical, no intersection
            return None

        horizontal_y = horizontal[self.KEY_POS_FROM][self.KEY_POS_Y]
        horizontal_from_x = horizontal[self.KEY_POS_FROM][self.KEY_POS_X]
        horizontal_to_x = horizontal[self.KEY_POS_TO][self.KEY_POS_X]
        vertical_x = vertical[self.KEY_POS_FROM][self.KEY_POS_X]
        vertical_from_y = vertical[self.KEY_POS_FROM][self.KEY_POS_Y]
        vertical_to_y = vertical[self.KEY_POS_TO][self.KEY_POS_Y]

        if min(vertical_from_y, vertical_to_y) < horizontal_y < max(vertical_from_y, vertical_to_y) \
                and min(horizontal_from_x, horizontal_to_x) < vertical_x < max(horizontal_from_x, horizontal_to_x):
            return {
                self.KEY_POS_X: vertical_x,
                self.KEY_POS_Y: horizontal_y
            }
        else:
            return None

################################################################################

def puzzle_1() -> None:
    """
    --- Part One ---

    The Document indicates that you should start at the given coordinates (where
    you just landed) and face North. Then, follow the provided sequence: either
    turn left (L) or right (R) 90 degrees, then walk forward the given number of
    blocks, ending at a new intersection.

    There's no time to follow such ridiculous instructions on foot, though, so
    you take a moment and work out the destination. Given that you can only walk
    on the street grid of the city, how far is the shortest path to the
    destination?

    For example:

    Following R2, L3 leaves you 2 blocks East and 3 blocks North, or 5 blocks
    away.
    R2, R2, R2 leaves you 2 blocks due South of your starting position, which is
    2 blocks away.
    R5, L5, R5, R3 leaves you 12 blocks away.
    How many blocks away is Easter Bunny HQ?
    """

    with open(join(getcwd(), SELF_DIR_NAME, INPUT_TXT_NAME), "r") as f:
        instructions = f.read().split(", ")
        santa = Santa()
        [santa.follow_instruction(instruction) for instruction in instructions]
        # should be 242 blocks
        print(santa.fake_hq_distance)

################################################################################

def puzzle_2() -> None:
    """
    --- Part Two ---
    
    Then, you notice the instructions continue on the back of the Recruiting
    Document. Easter Bunny HQ is actually at the first location you visit twice.

    For example, if your instructions are R8, R4, R4, R8, the first location you
    visit twice is 4 blocks away, due East.

    How many blocks away is the first location you visit twice?
    """

    with open(join(getcwd(), SELF_DIR_NAME, INPUT_TXT_NAME), "r") as f:
        instructions = f.read().split(", ")
        santa = Santa()
        [santa.follow_instruction(instruction) for instruction in instructions]
        # should be 150 blocks
        print(santa.real_hq_distance)

################################################################################