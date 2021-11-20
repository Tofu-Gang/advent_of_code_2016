__author__ = "Tofu Gang"
__email__ = "tofugangsw@gmail.com"

from os import getcwd
from os.path import join
from re import compile

"""
--- Day 4: Security Through Obscurity ---

Finally, you come across an information kiosk with a list of rooms. Of course, 
the list is encrypted and full of decoy data, but the instructions to decode the 
list are barely hidden nearby. Better remove the decoy data first.
"""

################################################################################

SELF_DIR_NAME = "day_04"
INPUT_TXT_NAME = "input.txt"

################################################################################

def _get_name(room: str) -> str:
    """
    :param room: encrypted line from the list of rooms
    :return: encrypted name of the room
    """

    return room.rsplit(sep="-", maxsplit=1)[0]

################################################################################

def _get_id(room: str) -> int:
    """
    :param room: encrypted line from the list of rooms
    :return: sector ID
    """

    pattern = compile(r'\d+')
    return int(pattern.search(room).group(0))

################################################################################

def _get_checksum(room: str) -> str:
    """
    :param room: encrypted line from the list of rooms
    :return: checksum
    """

    pattern = compile(r'\[[a-z]+]')
    return pattern.search(room).group(0)[1:-1]

################################################################################

def _is_real_room(room: str) -> bool:
    """
    :param room: encrypted line from the list of rooms
    :return: True if the room is real, False otherwise
    """

    name = _get_name(room)
    checksum = _get_checksum(room)
    quantities = sorted(
        [(chr(i), name.count(chr(i)))
         for i in range(ord("a"), ord("z") + 1)
         if name.count(chr(i)) > 0],
        key=lambda quantity: quantity[1],
        reverse=True)
    return all([checksum[i] == quantities[i][0] for i in range(len(checksum))])

################################################################################

def _decrypted_letter(letter: str, sector_id: int) -> str:
    """
    :param letter: one letter from an encrypted room name
    :param sector_id: room sector ID
    :return: decrypted letter
    """

    if letter == "-":
        return " "
    else:
        i = 0
        letter = ord(letter)
        while i < sector_id:
            letter += 1
            if letter > ord("z"):
                letter = ord("a")
            i += 1
        return chr(letter)

################################################################################

def _decrypted_name(room: str) -> str:
    """
    :param room: encrypted line from the list of rooms
    :return: decrypted name of the room
    """

    name = _get_name(room)
    sector_id = _get_id(room)
    return ''.join([_decrypted_letter(letter, sector_id) for word in name for letter in word])

################################################################################

def puzzle_1() -> None:
    """
    --- Part One ---

    Each room consists of an encrypted name (lowercase letters separated by
    dashes) followed by a dash, a sector ID, and a checksum in square brackets.

    A room is real (not a decoy) if the checksum is the five most common letters
    in the encrypted name, in order, with ties broken by alphabetization. For
    example:

    -aaaaa-bbb-z-y-x-123[abxyz] is a real room because the most common letters
     are a (5), b (3), and then a tie between x, y, and z, which are listed
     alphabetically.
    -a-b-c-d-e-f-g-h-987[abcde] is a real room because although the letters are
     all tied (1 of each), the first five are listed alphabetically.
    -not-a-real-room-404[oarel] is a real room.
    -totally-real-room-200[decoy] is not.

    Of the real rooms from the list above, the sum of their sector IDs is 1514.

    What is the sum of the sector IDs of the real rooms?
    """

    with open(join(getcwd(), SELF_DIR_NAME, INPUT_TXT_NAME), "r") as f:
        rooms = list(map(lambda room: room.strip(), f.readlines()))
        # should be 173787
        print(sum([_get_id(room) for room in rooms if _is_real_room(room)]))

################################################################################

def puzzle_2() -> None:
    """
    --- Part Two ---

    With all the decoy data out of the way, it's time to decrypt this list and
    get moving.

    The room names are encrypted by a state-of-the-art shift cipher, which is
    nearly unbreakable without the right software. However, the information
    kiosk designers at Easter Bunny HQ were not expecting to deal with a master
    cryptographer like yourself.

    To decrypt a room name, rotate each letter forward through the alphabet a
    number of times equal to the room's sector ID. A becomes B, B becomes C, Z
    becomes A, and so on. Dashes become spaces.

    For example, the real name for qzmt-zixmtkozy-ivhz-343 is very encrypted
    name.

    What is the sector ID of the room where North Pole objects are stored?
    """

    with open(join(getcwd(), SELF_DIR_NAME, INPUT_TXT_NAME), "r") as f:
        rooms = list(map(lambda room: room.strip(), f.readlines()))
        for room in rooms:
            name = _decrypted_name(room)
            if "north" in name:
                # should be 548
                print(_get_id(room))
                break

################################################################################
