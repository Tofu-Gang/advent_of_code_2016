__author__ = "Jakub Franěk"
__email__ = "tofugangsw@gmail.com"

"""
--- Day 8: Two-Factor Authentication ---

You come across a door implementing what you can only assume is an 
implementation of two-factor authentication after a long game of requirements 
telephone.

To get past the door, you first swipe a keycard (no problem; there was one on a 
nearby desk). Then, it displays a code on a little screen, and you type that 
code on a keypad. Then, presumably, the door unlocks.

Unfortunately, the screen has been smashed. After a few minutes, you've taken 
everything apart and figured out how it works. Now you just have to work out 
what the screen would have displayed.
"""

INPUT_FILE_PATH = "src/day_08/input.txt"


################################################################################

class Screen(object):
    WIDTH = 50
    HEIGHT = 6
    PIXEL_OFF = " "
    PIXEL_ON = "*"
    INSTRUCTION_RECT = "rect"
    INSTRUCTION_ROTATE_ROW = "rotate row"
    INSTRUCTION_ROTATE_COLUMN = "rotate column"

################################################################################

    def __init__(self):
        """
        The screen is 50 pixels wide and 6 pixels tall, all of which start off.
        """

        self._screen = [[self.PIXEL_OFF for _ in range(self.WIDTH)]
                        for _ in range(self.HEIGHT)]

################################################################################

    @property
    def pixels_on_count(self) -> int:
        """
        :return: number of lit pixels
        """

        return sum(row.count(self.PIXEL_ON) for row in self._screen)

################################################################################

    def process_instruction(self, instruction: str) -> None:
        """
        The screen is capable of three somewhat peculiar operations:

        -rect AxB turns on all of the pixels in a rectangle at the top-left of
         the screen which is A wide and B tall.
        -rotate row y=A by B shifts all of the pixels in row A (0 is the top
         row) right by B pixels. Pixels that would fall off the right end appear
         at the left end of the row.
        -rotate column x=A by B shifts all of the pixels in column A (0 is the
         left column) down by B pixels. Pixels that would fall off the bottom
         appear at the top of the column.

        :param instruction: instruction to be processed
        """

        if instruction.startswith(self.INSTRUCTION_RECT):
            # rect AxB
            params = instruction.split(" ")[1]
            width = int(params.split("x")[0])
            height = int(params.split("x")[1])
            self._rect(width, height)
        elif instruction.startswith(self.INSTRUCTION_ROTATE_ROW):
            # rotate row y=A by B
            row = int(instruction.split(" ")[2][2:])
            offset = int(instruction.split(" ")[4])
            self._rotate_row(row, offset)
        elif instruction.startswith(self.INSTRUCTION_ROTATE_COLUMN):
            # rotate column x=A by B
            column = int(instruction.split(" ")[2][2:])
            offset = int(instruction.split(" ")[4])
            self._rotate_column(column, offset)
        else:
            # shouldn't happen
            raise Exception()

################################################################################

    def print_message(self) -> None:
        """
        You notice that the screen is only capable of displaying capital
        letters; in the font it uses, each letter is 5 pixels wide and 6 tall.

        After you swipe your card, what code is the screen trying to display?
        """

        for row in range(self.HEIGHT):
            print("".join(self._screen[row]))

################################################################################

    def _pixel_on(self, row: int, column: int) -> None:
        """
        Turn on a specific pixel.

        :param row: pixel row
        :param column: pixel column
        """

        self._screen[row][column] = self.PIXEL_ON

################################################################################

    def _pixel_off(self, row: int, column: int) -> None:
        """
        Turn off a specific pixel.

        :param row: pixel row
        :param column: pixel column
        """

        self._screen[row][column] = self.PIXEL_OFF

################################################################################

    def _rect(self, width: int, height: int) -> None:
        """
        Instruction rect AxB turns on all of the pixels in a rectangle at the
        top-left of the screen which is A wide and B tall.

        :param width: rect width
        :param height: rect height
        """

        for row in range(height):
            for column in range(width):
                self._pixel_on(row, column)

################################################################################

    def _rotate_row(self, row: int, offset: int) -> None:
        """
        Instruction rotate row y=A by B shifts all of the pixels in row A (0 is
        the top row) right by B pixels. Pixels that would fall off the right
        end appear at the left end of the row.

        :param row: row to rotate
        :param offset: offset by which to rotate a specific row
        """

        offset %= self.WIDTH
        screen_row = self._screen[row]
        self._screen[row] = \
            screen_row[self.WIDTH - offset:] + screen_row[:self.WIDTH - offset]

################################################################################

    def _rotate_column(self, column: int, offset: int) -> None:
        """
        Instruction rotate column x=A by B shifts all of the pixels in column A
        (0 is the left column) down by B pixels. Pixels that would fall off the
        bottom appear at the top of the column.

        :param column: column to rotate
        :param offset: offset by which to rotate a specific column
        """

        offset %= self.HEIGHT
        screen_column = [self._screen[row][column]
                         for row in range(self.HEIGHT)]
        screen_column = \
            screen_column[self.HEIGHT - offset:] \
            + screen_column[:self.HEIGHT - offset]
        for row in range(self.HEIGHT):
            self._screen[row][column] = screen_column[row]


################################################################################

def puzzle_01() -> int:
    """
    The magnetic strip on the card you swiped encodes a series of instructions
    for the screen; these instructions are your puzzle input. The screen is 50
    pixels wide and 6 pixels tall, all of which start off, and is capable of
    three somewhat peculiar operations:

    -rect AxB turns on all of the pixels in a rectangle at the top-left of the
     screen which is A wide and B tall.
    -rotate row y=A by B shifts all of the pixels in row A (0 is the top row)
     right by B pixels. Pixels that would fall off the right end appear at the
     left end of the row.
    -rotate column x=A by B shifts all of the pixels in column A (0 is the left
     column) down by B pixels. Pixels that would fall off the bottom appear at
     the top of the column.

    For example, here is a simple sequence on a smaller screen:

    rect 3x2 creates a small rectangle in the top-left corner:

    ###....
    ###....
    .......

    rotate column x=1 by 1 rotates the second column down by one pixel:

    #.#....
    ###....
    .#.....

    rotate row y=0 by 4 rotates the top row right by four pixels:

    ....#.#
    ###....
    .#.....

    rotate column x=1 by 1 again rotates the second column down by one pixel,
    causing the bottom pixel to wrap back to the top:

    .#..#.#
    #.#....
    .#.....

    As you can see, this display technology is extremely powerful, and will soon
    dominate the tiny-code-displaying-screen market. That's what the
    advertisement on the back of the display tries to convince you, anyway.

    There seems to be an intermediate check of the voltage used by the display:
    after you swipe your card, if the screen did work, how many pixels should be
    lit?

    :return: number of lit pixels
    """

    with open(INPUT_FILE_PATH, "r") as f:
        instructions = f.readlines()
        screen = Screen()
        for instruction in instructions:
            screen.process_instruction(instruction)
        return screen.pixels_on_count


################################################################################

def puzzle_02() -> None:
    """
    You notice that the screen is only capable of displaying capital letters; in
    the font it uses, each letter is 5 pixels wide and 6 tall.

    After you swipe your card, what code is the screen trying to display?

    :return: None; Answer should be RURUCEOEIL and is displayed as an ASCII art.
    """

    with open(INPUT_FILE_PATH, "r") as f:
        instructions = f.readlines()
        screen = Screen()
        for instruction in instructions:
            screen.process_instruction(instruction)
        screen.print_message()


################################################################################
