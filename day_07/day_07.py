__author__ = "Tofu Gang"
__email__ = "tofugangsw@gmail.com"

from os import getcwd
from os.path import join
from re import compile
from typing import Tuple, Any, List
from itertools import product

"""
-- Day 7: Internet Protocol Version 7 ---

While snooping around the local network of EBHQ, you compile a list of IP 
addresses (they're IPv7, of course; IPv6 is much too limited). You'd like to 
figure out which IPs support TLS (transport-layer snooping).
"""

################################################################################

SELF_DIR_NAME = "day_07"
INPUT_TXT_NAME = "input.txt"

################################################################################

def _get_hypernet_sequences(address: str) -> Tuple[Any]:
    """
    :param address: one IPv7 address from the puzzle input
    :return: hypernet sequences from the address
    """

    pattern = compile(r'\[.+?]')
    return tuple(pattern.findall(address))

################################################################################

def _get_supernet_sequences(address: str) -> Tuple[str]:
    """
    :param address: one IPv7 address from the puzzle input
    :return: supernet sequences from the address
    """

    separator = " "
    supernet_sequences = address

    for hypernet_sequence in _get_hypernet_sequences(address):
        supernet_sequences = supernet_sequences.replace(hypernet_sequence, separator)
    return tuple(supernet_sequences.split(separator))

################################################################################

def _is_abba_in_sequence(sequence: str) -> bool:
    """
    :param sequence: a part of an IPv7 address from the puzzle input, either a
    hypernet or a supernet sequence
    :return: True if there is ABBA (Autonomous Bridge Bypass Annotation) in the
    sequence, False otherwise
    """

    return any(
        [sequence[i] != sequence[i + 1]
         and sequence[i] == sequence[i + 3]
         and sequence[i + 1] == sequence[i + 2]
         for i in range(len(sequence) - 3)])

################################################################################

def _supports_tls(address: str) -> bool:
    """
    :param address: one IPv7 address from the puzzle input
    :return: True if the address supports TLS (transport-layer snooping), False
    otherwise
    """

    return not any([_is_abba_in_sequence(sequence)
                    for sequence in _get_hypernet_sequences(address)]) \
           and any([_is_abba_in_sequence(part)
                    for part in _get_supernet_sequences(address)])

################################################################################

def _get_aba_sequences(address: str) -> List[str]:
    """
    :param address: one IPv7 address from the puzzle input
    :return: ABA (Area-Broadcast Accessor) or None, if ABA is not found
    """

    sequences = _get_supernet_sequences(address)
    aba = []

    for sequence in sequences:
        for i in range(len(sequence) - 2):
            if sequence[i] != sequence[i + 1] and sequence[i] == sequence[i + 2]:
                aba.append(sequence[i:i + 3])
    return aba

################################################################################

def _get_bab_sequences(address: str) -> List[str]:
    """
    :param address: one IPv7 address from the puzzle input
    :return: BAB (Byte Allocation Block) or None, if BAB is not found
    """

    sequences = _get_hypernet_sequences(address)
    bab = []

    for sequence in sequences:
        for i in range(len(sequence) - 2):
            if sequence[i] == sequence[i + 2] and sequence[i] != sequence[i + 1]:
                bab.append(sequence[i: i + 3])
    return bab

################################################################################

def _supports_ssl(address: str) -> bool:
    """
    :param address: one IPv7 address from the puzzle input
    :return: True if the address supports SSL (super-secret listening), False
    otherwise
    """

    aba_sequences = _get_aba_sequences(address)
    bab_sequences = _get_bab_sequences(address)
    return any([
        combination[0][0] == combination[1][1]
        and combination[0][1] == combination[1][0]
        for combination in product(aba_sequences, bab_sequences)])

################################################################################

def puzzle_1() -> None:
    """
    --- Part One ---

    An IP supports TLS if it has an Autonomous Bridge Bypass Annotation, or
    ABBA. An ABBA is any four-character sequence which consists of a pair of two
    different characters followed by the reverse of that pair, such as xyyx or
    abba. However, the IP also must not have an ABBA within any hypernet
    sequences, which are contained by square brackets.

    For example:

    -abba[mnop]qrst supports TLS (abba outside square brackets).
    -abcd[bddb]xyyx does not support TLS (bddb is within square brackets, even
     though xyyx is outside square brackets).
    -aaaa[qwer]tyui does not support TLS (aaaa is invalid; the interior
     characters must be different).
    -ioxxoj[asdfgh]zxcvbn supports TLS (oxxo is outside square brackets, even
     though it's within a larger string).

    How many IPs in your puzzle input support TLS?
    """

    with open(join(getcwd(), SELF_DIR_NAME, INPUT_TXT_NAME), "r") as f:
        addresses = list([address.strip() for address in f.readlines()])
        # should be 115
        print(len(list(filter(_supports_tls, addresses))))

################################################################################

def puzzle_2() -> None:
    """
    --- Part Two ---

    You would also like to know which IPs support SSL (super-secret listening).

    An IP supports SSL if it has an Area-Broadcast Accessor, or ABA, anywhere in
    the supernet sequences (outside any square bracketed sections), and a
    corresponding Byte Allocation Block, or BAB, anywhere in the hypernet
    sequences. An ABA is any three-character sequence which consists of the same
    character twice with a different character between them, such as xyx or aba.
    A corresponding BAB is the same characters but in reversed positions: yxy
    and bab, respectively.

    For example:

    -aba[bab]xyz supports SSL (aba outside square brackets with corresponding
     bab within square brackets).
    -xyx[xyx]xyx does not support SSL (xyx, but no corresponding yxy).
    -aaa[kek]eke supports SSL (eke in supernet with corresponding kek in
     hypernet; the aaa sequence is not related, because the interior character
     must be different).
    -zazbz[bzb]cdb supports SSL (zaz has no corresponding aza, but zbz has a
     corresponding bzb, even though zaz and zbz overlap).

    How many IPs in your puzzle input support SSL?
    """

    with open(join(getcwd(), SELF_DIR_NAME, INPUT_TXT_NAME), "r") as f:
        addresses = list([address.strip() for address in f.readlines()])
        # should be 231
        print(len(list(filter(_supports_ssl, addresses))))

################################################################################
