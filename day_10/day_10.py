__author__ = "Tofu Gang"
__email__ = "tofugangsw@gmail.com"

from os import getcwd
from os.path import join
from re import compile

"""
--- Day 10: Balance Bots ---

You come upon a factory in which many robots are zooming around handing small 
microchips to each other.
"""

################################################################################

SELF_DIR_NAME = "day_10"
INPUT_TXT_NAME = "input.txt"
VALUE_PREFIX = "value"
BOT_PREFIX = "bot"
GIVE_LOW_TO_BOT = "gives low to bot"
GIVE_LOW_TO_OUTPUT = "gives low to output"
GIVE_HIGH_TO_BOT = "and high to bot"
GIVE_HIGH_TO_OUTPUT = "and high to output"

################################################################################

class Bot(object):
    GOAL_MICROCHIP_1 = 61
    GOAL_MICROCHIP_2 = 17

################################################################################

    def __init__(self, name: int):
        """
        :param name: bot name
        """

        self._name = name
        self._microchips = []
        self._is_goal_bot = False

################################################################################

    @property
    def name(self) -> int:
        """
        :return:
        """

        return self._name

################################################################################

    @property
    def is_goal_bot(self) -> bool:
        """
        :return:
        """

        return self._is_goal_bot

################################################################################

    @property
    def has_two(self) -> bool:
        """
        :return:
        """

        return len(self._microchips) == 2

################################################################################

    def take_microchip(self, microchip: int) -> None:
        """
        :param microchip: microchip value
        """

        self._microchips.append(microchip)

################################################################################

    def give_low(self) -> int:
        """
        :return:
        """

        if not self._is_goal_bot:
            self._is_goal_bot = self.GOAL_MICROCHIP_1 in self._microchips \
                                and self.GOAL_MICROCHIP_2 in self._microchips

        microchip = min(self._microchips)
        self._microchips.remove(microchip)
        return microchip

################################################################################

    def give_high(self) -> int:
        """
        :return:
        """

        if not self._is_goal_bot:
            self._is_goal_bot = self.GOAL_MICROCHIP_1 in self._microchips \
                                and self.GOAL_MICROCHIP_2 in self._microchips

        microchip = max(self._microchips)
        self._microchips.remove(microchip)
        return microchip

################################################################################

def puzzle_1() -> None:
    """
    --- Part One ---

    Upon closer examination, you notice that each bot only proceeds when it has
    two microchips, and once it does, it gives each one to a different bot or
    puts it in a marked "output" bin. Sometimes, bots take microchips from
    "input" bins, too.

    Inspecting one of the microchips, it seems like they each contain a single
    number; the bots must use some logic to decide what to do with each chip.
    You access the local control computer and download the bots' instructions
    (your puzzle input).

    Some of the instructions specify that a specific-valued microchip should be
    given to a specific bot; the rest of the instructions indicate what a given
    bot should do with its lower-value or higher-value chip.

    For example, consider the following instructions:

    -value 5 goes to bot 2
    -bot 2 gives low to bot 1 and high to bot 0
    -value 3 goes to bot 1
    -bot 1 gives low to output 1 and high to bot 0
    -bot 0 gives low to output 2 and high to output 0
    -value 2 goes to bot 2

    -Initially, bot 1 starts with a value-3 chip, and bot 2 starts with a
     value-2 chip and a value-5 chip.
    -Because bot 2 has two microchips, it gives its lower one (2) to bot 1 and
     its higher one (5) to bot 0.
    -Then, bot 1 has two microchips; it puts the value-2 chip in output 1 and
     gives the value-3 chip to bot 0.
    -Finally, bot 0 has two microchips; it puts the 3 in output 2 and the 5 in
     output 0.

    In the end, output bin 0 contains a value-5 microchip, output bin 1 contains
    a value-2 microchip, and output bin 2 contains a value-3 microchip. In this
    configuration, bot number 2 is responsible for comparing value-5 microchips
    with value-2 microchips.

    Based on your instructions, what is the number of the bot that is
    responsible for comparing value-61 microchips with value-17 microchips?
    """

    with open(join(getcwd(), SELF_DIR_NAME, INPUT_TXT_NAME), "r") as f:
        instructions = list([instruction.strip() for instruction in f.readlines()])
        bots = []
        number_pattern = compile("\d+")
        value_instructions = [instruction for instruction in instructions if instruction.startswith(VALUE_PREFIX)]

        for instruction in value_instructions:
            number_pattern_result = number_pattern.findall(instruction)
            microchip_value = int(number_pattern_result[0])
            bot_name = number_pattern_result[1]

            try:
                bot = tuple(filter(lambda bot: bot.name == bot_name, bots))[0]
            except IndexError:
                bot = Bot(bot_name)
                bots.append(bot)

            if not bot.has_two:
                bot.take_microchip(microchip_value)
                instructions.remove(instruction)

        while not any([bot.is_goal_bot for bot in bots]):
            active_bot = tuple(filter(lambda bot: bot.has_two, bots))[0]
            instruction = tuple(filter(lambda instruction: number_pattern.findall(instruction)[0] == str(active_bot.name), instructions))[0]

            if GIVE_LOW_TO_BOT in instruction:
                bot_dest_name = number_pattern.findall(instruction)[1]
                try:
                    bot_dest = tuple(filter(lambda bot: bot.name == bot_dest_name, bots))[0]
                except IndexError:
                    bot_dest = Bot(bot_dest_name)
                    bots.append(bot_dest)
                microchip = active_bot.give_low()
                bot_dest.take_microchip(microchip)
            elif GIVE_LOW_TO_OUTPUT in instruction:
                active_bot.give_low()
            else:
                # shouldn't happen
                raise Exception()

            if GIVE_HIGH_TO_BOT in instruction:
                bot_dest_name = number_pattern.findall(instruction)[2]
                try:
                    bot_dest = tuple(filter(lambda bot: bot.name == bot_dest_name, bots))[0]
                except IndexError:
                    bot_dest = Bot(bot_dest_name)
                    bots.append(bot_dest)
                microchip = active_bot.give_high()
                bot_dest.take_microchip(microchip)
            elif GIVE_HIGH_TO_OUTPUT in instruction:
                active_bot.give_high()
            else:
                # shouldn't happen
                raise Exception()

            instructions.remove(instruction)

        # should be 118
        print([bot.name for bot in bots if bot.is_goal_bot][0])

################################################################################

def puzzle_2() -> None:
    """
    --- Part Two ---

    What do you get if you multiply together the values of one chip in each of
    outputs 0, 1, and 2?
    """

    with open(join(getcwd(), SELF_DIR_NAME, INPUT_TXT_NAME), "r") as f:
        instructions = list([instruction.strip() for instruction in f.readlines()])
        bots = []
        number_pattern = compile("\d+")
        value_instructions = [instruction for instruction in instructions if instruction.startswith(VALUE_PREFIX)]
        output_0 = None
        output_1 = None
        output_2 = None

        for instruction in value_instructions:
            number_pattern_result = number_pattern.findall(instruction)
            microchip_value = int(number_pattern_result[0])
            bot_name = number_pattern_result[1]

            try:
                bot = tuple(filter(lambda bot: bot.name == bot_name, bots))[0]
            except IndexError:
                bot = Bot(bot_name)
                bots.append(bot)

            if not bot.has_two:
                bot.take_microchip(microchip_value)
                instructions.remove(instruction)

        while output_0 is None or output_1 is None or output_2 is None:
            active_bot = tuple(filter(lambda bot: bot.has_two, bots))[0]
            instruction = tuple(filter(lambda instruction: number_pattern.findall(instruction)[0] == str(active_bot.name), instructions))[0]

            if GIVE_LOW_TO_BOT in instruction:
                bot_dest_name = number_pattern.findall(instruction)[1]
                try:
                    bot_dest = tuple(filter(lambda bot: bot.name == bot_dest_name, bots))[0]
                except IndexError:
                    bot_dest = Bot(bot_dest_name)
                    bots.append(bot_dest)
                microchip = active_bot.give_low()
                bot_dest.take_microchip(microchip)
            elif GIVE_LOW_TO_OUTPUT in instruction:
                microchip = active_bot.give_low()
                output_name = number_pattern.findall(instruction)[1]
                if output_name == "0":
                    output_0 = microchip
                elif output_name == "1":
                    output_1 = microchip
                elif output_name == "2":
                    output_2 = microchip
            else:
                # shouldn't happen
                raise Exception()

            if GIVE_HIGH_TO_BOT in instruction:
                bot_dest_name = number_pattern.findall(instruction)[2]
                try:
                    bot_dest = tuple(filter(lambda bot: bot.name == bot_dest_name, bots))[0]
                except IndexError:
                    bot_dest = Bot(bot_dest_name)
                    bots.append(bot_dest)
                microchip = active_bot.give_high()
                bot_dest.take_microchip(microchip)
            elif GIVE_HIGH_TO_OUTPUT in instruction:
                microchip = active_bot.give_high()
                output_name = number_pattern.findall(instruction)[2]
                if output_name == "0":
                    output_0 = microchip
                elif output_name == "1":
                    output_1 = microchip
                elif output_name == "2":
                    output_2 = microchip
            else:
                # shouldn't happen
                raise Exception()

            instructions.remove(instruction)

        # should be 143153
        print(output_0 * output_1 * output_2)

################################################################################
