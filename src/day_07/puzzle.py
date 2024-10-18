__author__ = "Jakub Franěk"
__email__ = "tofugangsw@gmail.com"

"""
--- Day 7: Internet Protocol Version 7 ---

While snooping around the local network of EBHQ, you compile a list of IP 
addresses (they're IPv7, of course; IPv6 is much too limited). You'd like to 
figure out which IPs support TLS (transport-layer snooping).
"""

from re import compile
from itertools import product

INPUT_FILE_PATH = "src/day_07/input.txt"


################################################################################

class Address(object):

    def __init__(self, address):
        """
        Hypernet sequences are contained by square brackets.
        Supernet sequences are outside any square bracketed sections.
        An ABA, or Area-Broadcast Accessor, is any three-character sequence
        which consists of the same character twice with a different character
        between them. Found in the supernet sequences.
        A BAB, or Byte Allocation Block, is any three-character sequence which
        consists of the same character twice with a different character between
        them. Found in the hypernet sequences.

        :param address: one IPv7 address from the puzzle input
        """
        self._hypernet_sequences = tuple(compile(r'\[(.+?)]').findall(address))
        self._supernet_sequences = tuple(
            "".join(match)
            for match in compile(r"^(.+?)\[|](.+?)\[|](.+?)$").findall(address))
        self._aba_sequences = tuple(
            sequence[i:i + 3]
            for sequence in self._supernet_sequences
            for i in range(len(sequence) - 2)
            if sequence[i] != sequence[i + 1]
            and sequence[i] == sequence[i + 2])
        self._bab_sequences = tuple(
            sequence[i:i + 3]
            for sequence in self._hypernet_sequences
            for i in range(len(sequence) - 2)
            if sequence[i] != sequence[i + 1]
            and sequence[i] == sequence[i + 2])

################################################################################

    @staticmethod
    def _is_abba_in_sequence(sequence: str) -> bool:
        """
        ABBA, or Autonomous Bridge Bypass Annotation, is a four-character
        sequence which consists of a pair of two different characters followed
        by the reverse of that pair.

        :param sequence: a part of an IPv7 address from the puzzle input, either
        a hypernet or a supernet sequence
        :return: True if there is ABBA in the sequence, False otherwise
        """

        return any(sequence[i] != sequence[i + 1]
                   and sequence[i] == sequence[i + 3]
                   and sequence[i + 1] == sequence[i + 2]
                   for i in range(len(sequence) - 3))

################################################################################

    @property
    def supports_tls(self) -> bool:
        """
        An address supports TLS, or Transport-Layer Snooping, if it contains at
        least one ABBA in the supernet sequences and no ABBA in the hypernet
        sequences.

        :return: True if the address supports TLS, False otherwise
        """

        return (
                not any(self._is_abba_in_sequence(sequence)
                        for sequence in self._hypernet_sequences)
                and any(self._is_abba_in_sequence(sequence)
                        for sequence in self._supernet_sequences))

################################################################################

    @property
    def supports_ssl(self) -> bool:
        """
        An IP supports SSL, or Super-Secret Listening, if it has an
        Area-Broadcast Accessor, or ABA, anywhere in the supernet sequences, and
        a corresponding Byte Allocation Block, or BAB, anywhere in the hypernet
        sequences.

        :return: True if the address supports SSL, False otherwise
        """

        return any(
            aba[0] == bab[1] and aba[1] == bab[0]
            for aba, bab in product(self._aba_sequences, self._bab_sequences))


################################################################################

def puzzle_01() -> int:
    """
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

    :return: How many IPs in your puzzle input support TLS?
    """

    with open(INPUT_FILE_PATH, "r") as f:
        addresses = [Address(address) for address in f.readlines()]
        return len(tuple(filter(
            lambda address: address.supports_tls, addresses)))


################################################################################

def puzzle_02() -> int:
    """
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

    :return: How many IPs in your puzzle input support SSL?
    """

    with open(INPUT_FILE_PATH, "r") as f:
        addresses = [Address(address) for address in f.readlines()]
        return len(tuple(filter(
            lambda address: address.supports_ssl, addresses)))

################################################################################
