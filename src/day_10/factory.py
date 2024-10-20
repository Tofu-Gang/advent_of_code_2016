__author__ = "Jakub Franěk"
__email__ = "tofugangsw@gmail.com"

from re import compile
from typing import Dict
from numpy import prod


################################################################################
class Factory:
    INPUT_FILE_PATH = "src/day_10/input.txt"
    GOAL_VALUES = (61, 17)
    GOAL_OUTPUTS = (0, 1, 2)
    NUMBER_PATTERN = compile(r"(\d+)")
    INITIAL_KEYWORD = "value"
    GIVE_KEYWORD = "give"
    BOT_KEYWORD = "bot"
    LOW_BOT_PHRASE = "low to bot"
    LOW_OUTPUT_PHRASE = "low to output"
    HIGH_BOT_PHRASE = "high to bot"
    HIGH_OUTPUT_PHRASE = "high to output"
    LOW_KEYWORD = "low"
    HIGH_KEYWORD = "high"

################################################################################

    def __init__(self):
        """
        Create a factory with:
        -dict of bots, where keys are bot numbers and values are lists of
         microchip values they are currently holding
        -dict of outputs, where keys are output numbers and values are microchip
         values in the output bin
        -dict of instructions, where keys are bot numbers and values are another
         dict that represents the actual instruction: keys are strings
         representing the instruction (give low/high to bot/output) and values
         are numbers of the target bot/output
        """

        self._bots = {}
        self._output = {}
        self._process_initial_instructions()
        self._instructions = self._create_give_instructions()
        self._goal_bot = None

################################################################################

    def run_instructions(self) -> None:
        """
        Process all the instructions so the bots move the microchips.
        """

        while len(self._instructions) > 0:
            self._move_microchip()

################################################################################

    @property
    def goal_bot(self) -> int:
        """
        :return: number of the bot that is responsible for comparing goal value
        microchips
        """

        return self._goal_bot

################################################################################

    @property
    def goal_product(self) -> int:
        """
        :return: product of values from goal outputs
        """

        return prod(tuple(self._output[index] for index in self.GOAL_OUTPUTS))

################################################################################

    def _process_initial_instructions(self) -> None:
        """
        Filter out the instructions where bots take microchips from input bins
        and process those instructions.
        """

        with open(self.INPUT_FILE_PATH, "r") as f:
            lines = f.readlines()
            # filter out only instructions where a bot takes an input value
            instructions = filter(
                lambda line: self.INITIAL_KEYWORD in line, lines)

            # give values to bots according to instructions
            for instruction in instructions:
                value, bot = tuple(
                    map(int, self.NUMBER_PATTERN.findall(instruction)))
                self._give_value_to_bot(bot, value)

################################################################################

    def _create_give_instructions(self) -> Dict[int, Dict[str, int]]:
        """
        Create dict of instructions, where keys are bot numbers and values are
        another dict that represents the actual instruction: keys are strings
        representing the instruction (give low/high to bot/output) and values
        are numbers of the target bot/output.
        """

        with open(self.INPUT_FILE_PATH, "r") as f:
            lines = f.readlines()
            instructions = {}

            for instruction in filter(
                    lambda line: self.GIVE_KEYWORD in line, lines):
                # get bot number and numbers of target bots/outputs for low and
                # high values
                bot, low, high = tuple(
                    map(int, self.NUMBER_PATTERN.findall(instruction)))
                # every instruction has all four combinations of give low/high
                # to bot/output; None is stored under keys that do not apply
                instructions[bot] = {
                    self.LOW_BOT_PHRASE:
                        low if self.LOW_BOT_PHRASE in instruction else None,
                    self.LOW_OUTPUT_PHRASE:
                        low if self.LOW_OUTPUT_PHRASE in instruction else None,
                    self.HIGH_BOT_PHRASE:
                        high if self.HIGH_BOT_PHRASE in instruction else None,
                    self.HIGH_OUTPUT_PHRASE:
                        high if self.HIGH_OUTPUT_PHRASE in instruction else None
                }

            return instructions

################################################################################

    def _give_value_to_bot(self, bot: int, value: int) -> None:
        """
        Give a microchip value to a specified bot. If this bot does not exist
        yet, create it.

        :param bot: bot number
        :param value: microchip value
        """

        if bot not in self._bots:
            # the bot does not exist yet, create it
            self._bots[bot] = []
        self._bots[bot].append(value)

################################################################################

    def _move_microchip(self) -> None:
        """
        Find a bot that has two microchips; find the instruction for this bot;
        process the instruction and give the microchips to other bots/outputs.
        """

        # find a bot that has two microchips
        bot = next(filter(lambda key: len(self._bots[key]) == 2, self._bots))
        values = self._bots[bot]

        if all(value in self.GOAL_VALUES for value in values):
            # bot that is responsible for comparing goal value microchips found
            self._goal_bot = bot
        # find the instruction for this bot
        instruction = self._instructions[bot]

        # process the instruction and give the microchips to other bots/outputs
        if instruction[self.LOW_BOT_PHRASE] is not None:
            low_bot = instruction[self.LOW_BOT_PHRASE]
            self._give_value_to_bot(low_bot, min(values))
        else:
            low_output = instruction[self.LOW_OUTPUT_PHRASE]
            self._output[low_output] = min(values)
        if instruction[self.HIGH_BOT_PHRASE] is not None:
            high_bot = instruction[self.HIGH_BOT_PHRASE]
            self._give_value_to_bot(high_bot, max(values))
        else:
            high_output = instruction[self.HIGH_OUTPUT_PHRASE]
            self._output[high_output] = max(values)

        self._bots[bot].clear()
        # remove the instruction
        del self._instructions[bot]

################################################################################
