__author__ = "Jakub Franěk"
__email__ = "tofugangsw@gmail.com"

"""
--- Day 1: No Time for a Taxicab ---

You're airdropped near Easter Bunny Headquarters in a city somewhere. "Near", 
unfortunately, is as close as you can get - the instructions on the Easter Bunny 
Recruiting Document the Elves intercepted start here, and nobody had time to 
work them out further.
"""

from typing import Dict, Union


################################################################################

class Santa(object):
    INPUT_FILE_PATH = "src/day_01/input.txt"
    KEY_POS_FROM = "FROM"
    KEY_POS_TO = "TO"
    KEY_POS_X = "X"
    KEY_POS_Y = "Y"
    TURN_LEFT = "L"
    TURN_RIGHT = "R"

    MOVEMENT = {
        TURN_LEFT: lambda direction: (direction - 1) % 4,
        TURN_RIGHT: lambda direction: (direction + 1) % 4,
        # north
        0: lambda x, y, blocks: (x, y + blocks),
        # east
        1: lambda x, y, blocks: (x + blocks, y),
        # south
        2: lambda x, y, blocks: (x, y - blocks),
        # west
        3: lambda x, y, blocks: (x - blocks, y)
    }

################################################################################

    def __init__(self):
        """
        Santa starts at position [0, 0], facing north. X-axis grows towards
        east, Y-axis grows towards north.
        """

        with open(self.INPUT_FILE_PATH, "r") as f:
            self._instructions = f.read().strip().split(", ")
            self._direction = 0
            self._posX = 0
            self._posY = 0
            self._paths = []
            self._headquarters = None

################################################################################

    @property
    def fake_hq_distance(self) -> int:
        """
        :return: shortest (Manhattan) distance to the Easter Bunny HQ in blocks,
        according to the part one of the puzzle
        """

        return abs(self._posX) + abs(self._posY)

################################################################################

    @property
    def real_hq_distance(self) -> int:
        """
        :return: shortest (Manhattan) distance to the Easter Bunny HQ in blocks,
        according to the part two of the puzzle
        """

        return (abs(self._headquarters[self.KEY_POS_X])
                + abs(self._headquarters[self.KEY_POS_Y]))

################################################################################

    def follow_instructions(self) -> None:
        """
        Follow the provided sequence of instructions.
        """

        for instruction in self._instructions:
            turn = instruction[0]
            blocks = int(instruction[1:])
            # turn left or right
            self._direction = self.MOVEMENT[turn](self._direction)

            pos_from = self._position()
            # walk forward the given number of blocks
            self._posX, self._posY = self.MOVEMENT[self._direction](
                self._posX, self._posY, blocks)
            pos_to = self._position()

            new_path = {
                self.KEY_POS_FROM: pos_from,
                self.KEY_POS_TO: pos_to
            }
            self._paths.append(new_path)

            if self._headquarters is None:
                try:
                    self._headquarters = next(filter(
                        lambda intersection: intersection is not None,
                        [self._intersection(new_path, path)
                         for path in self._paths]))
                except StopIteration:
                    # no intersection found yet
                    pass

################################################################################

    def _position(self) -> Dict[str, int]:
        """
        :return: current Santa's position
        """

        return {
            self.KEY_POS_X: self._posX,
            self.KEY_POS_Y: self._posY
        }

################################################################################

    def _is_path_horizontal(self, path: Dict[str, Dict[str, int]]) -> bool:
        """
        :param path: path which orientation we test
        :return: True if the path is horizontal, False otherwise
        """

        return (path[self.KEY_POS_FROM][self.KEY_POS_Y]
                == path[self.KEY_POS_TO][self.KEY_POS_Y])

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

        if (self._is_path_horizontal(path_1)
                and not self._is_path_horizontal(path_2)):
            horizontal = path_1
            vertical = path_2
        elif (self._is_path_horizontal(path_2)
              and not self._is_path_horizontal(path_1)):
            horizontal = path_2
            vertical = path_1
        else:
            # both paths are either horizontal or vertical, no intersection
            return None

        horizontal_y = horizontal[self.KEY_POS_FROM][self.KEY_POS_Y]
        horizontal_from_x = horizontal[self.KEY_POS_FROM][self.KEY_POS_X]
        horizontal_to_x = horizontal[self.KEY_POS_TO][self.KEY_POS_X]
        vertical_x = vertical[self.KEY_POS_FROM][self.KEY_POS_X]
        vertical_from_y = vertical[self.KEY_POS_FROM][self.KEY_POS_Y]
        vertical_to_y = vertical[self.KEY_POS_TO][self.KEY_POS_Y]

        if (min(vertical_from_y, vertical_to_y) < horizontal_y
                < max(vertical_from_y, vertical_to_y)
                and min(horizontal_from_x, horizontal_to_x) < vertical_x
                < max(horizontal_from_x, horizontal_to_x)):
            return {
                self.KEY_POS_X: vertical_x,
                self.KEY_POS_Y: horizontal_y
            }
        else:
            return None


################################################################################

def puzzle_01() -> int:
    """
    The Document indicates that you should start at the given coordinates (where
    you just landed) and face North. Then, follow the provided sequence: either
    turn left (L) or right (R) 90 degrees, then walk forward the given number of
    blocks, ending at a new intersection.

    There's no time to follow such ridiculous instructions on foot, though, so
    you take a moment and work out the destination. Given that you can only walk
    on the street grid of the city, how far is the shortest path to the
    destination?

    For example:

    -Following R2, L3 leaves you 2 blocks East and 3 blocks North, or 5 blocks
     away.
    -R2, R2, R2 leaves you 2 blocks due South of your starting position, which
     is 2 blocks away.
    -R5, L5, R5, R3 leaves you 12 blocks away.

    :return: How many blocks away is Easter Bunny HQ?
    """

    santa = Santa()
    santa.follow_instructions()
    return santa.fake_hq_distance


################################################################################

def puzzle_02() -> int:
    """
    Then, you notice the instructions continue on the back of the Recruiting
    Document. Easter Bunny HQ is actually at the first location you visit twice.

    For example, if your instructions are R8, R4, R4, R8, the first location you
    visit twice is 4 blocks away, due East.

    :return: How many blocks away is the first location you visit twice?
    """

    santa = Santa()
    santa.follow_instructions()
    return santa.real_hq_distance

################################################################################
