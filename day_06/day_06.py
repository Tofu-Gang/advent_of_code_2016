__author__ = "Tofu Gang"
__email__ = "tofugangsw@gmail.com"

from os import getcwd
from os.path import join

"""
--- Day 6: Signals and Noise ---

Something is jamming your communications with Santa. Fortunately, your signal is 
only partially jammed, and protocol in situations like this is to switch to a 
simple repetition code to get the message through.

In this model, the same message is sent repeatedly. You've recorded the 
repeating message signal (your puzzle input), but the data seems quite 
corrupted - almost too badly to recover. Almost.
"""

################################################################################

SELF_DIR_NAME = "day_06"
INPUT_TXT_NAME = "input.txt"

################################################################################

def puzzle_1() -> None:
    """
    --- Part One ---

    All you need to do is figure out which character is most frequent for each
    position. For example, suppose you had recorded the following messages:

    eedadn
    drvtee
    eandsr
    raavrd
    atevrs
    tsrnev
    sdttsa
    rasrtv
    nssdts
    ntnada
    svetve
    tesnvt
    vntsnd
    vrdear
    dvrsen
    enarar

    The most common character in the first column is e; in the second, a; in the
    third, s, and so on. Combining these characters returns the error-corrected
    message, easter.

    Given the recording in your puzzle input, what is the error-corrected
    version of the message being sent?
    """

    with open(join(getcwd(), SELF_DIR_NAME, INPUT_TXT_NAME), "r") as f:
        lines = list([line.strip() for line in f.readlines()])
        quantities = {}
        message = ""

        for i in range(len(lines[0])):
            # reset the quantities dict so every character has count of zero
            [quantities.update({chr(i): 0}) for i in range(ord("a"), ord("z") + 1)]

            for line in lines:
                # count all characters in the column number i
                quantities[line[i]] += 1

            for key in quantities:
                # find the most common character in the column number i
                if quantities[key] == max(quantities.values()):
                    message += key
                    break

        # should be kqsdmzft
        print(message)

################################################################################

def puzzle_2() -> None:
    """
    --- Part Two ---

    Of course, that would be the message - if you hadn't agreed to use a
    modified repetition code instead.

    In this modified code, the sender instead transmits what looks like random
    data, but for each character, the character they actually want to send is
    slightly less likely than the others. Even after signal-jamming noise, you
    can look at the letter distributions in each column and choose the least
    common letter to reconstruct the original message.

    In the above example, the least common character in the first column is a;
    in the second, d, and so on. Repeating this process for the remaining
    characters produces the original message, advent.

    Given the recording in your puzzle input and this new decoding methodology,
    what is the original message that Santa is trying to send?
    """

    with open(join(getcwd(), SELF_DIR_NAME, INPUT_TXT_NAME), "r") as f:
        lines = list([line.strip() for line in f.readlines()])
        quantities = {}
        message = ""

        for i in range(len(lines[0])):
            # reset the quantities dict so every character has count of zero
            [quantities.update({chr(i): 0}) for i in
             range(ord("a"), ord("z") + 1)]

            for line in lines:
                # count all characters in the column number i
                quantities[line[i]] += 1

            for key in quantities:
                # find the least common character in the column number i
                if quantities[key] == min(quantities.values()):
                    message += key
                    break

        # should be tpooccyo
        print(message)

################################################################################
