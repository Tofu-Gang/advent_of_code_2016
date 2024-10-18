__author__ = "Jakub Franěk"
__email__ = "tofugangsw@gmail.com"

"""
--- Day 4: Security Through Obscurity ---

Finally, you come across an information kiosk with a list of rooms. Of course, 
the list is encrypted and full of decoy data, but the instructions to decode the 
list are barely hidden nearby. Better remove the decoy data first.
"""

from re import compile

INPUT_FILE_PATH = "src/day_04/input.txt"
GOAL_DECRYPTED_ROOM_NAME = "northpole object storage"


################################################################################

class Room(object):

    def __init__(self, room_line: str):
        """
        Get encrypted name, sector id, checksum, information whether the room is
        real or not and decrypted name. The properties of this object will then
        return these precomputed values.
        """

        self._room_line = room_line
        self._sector_id = int(compile(r'\d+').findall(self._room_line)[0])
        self._name, self._checksum = self._room_line.split(str(self._sector_id))
        self._name = " ".join(self._name.split("-"))
        # omit the square brackets from the checksum
        self._checksum = self._checksum[1:-2]
        quantities = sorted([(chr(i), self._name.count(chr(i)))
                             for i in range(ord("a"), ord("z") + 1)],
                            key=lambda quantity: quantity[1], reverse=True)
        self._is_real = all([self._checksum[i] == quantities[i][0]
                             for i in range(len(self._checksum))])
        self._decrypted_name = " ".join(
            "".join(map(self._decrypted_letter, word))
            for word in self._name.split())

################################################################################

    @property
    def name(self) -> str:
        """
        :return: encrypted name of the room
        """

        return self._name

################################################################################

    @property
    def sector_id(self) -> int:
        """
        :return: sector ID
        """

        return self._sector_id

################################################################################

    @property
    def checksum(self) -> str:
        """
        :return: checksum
        """

        return self._checksum

################################################################################

    @property
    def is_real(self) -> bool:
        """
        :return: True if the room is real, False otherwise
        """

        return self._is_real

################################################################################

    @property
    def decrypted_name(self) -> str:
        """
        :return: decrypted name of the room
        """

        return self._decrypted_name

################################################################################

    def _decrypted_letter(self, letter: str) -> str:
        """
        :param letter: one letter from an encrypted room name
        :return: decrypted letter
        """

        letter = ord(letter)
        letter += self.sector_id % (ord("z") - ord("a") + 1)
        if letter > ord("z"):
            letter -= (ord("z") - ord("a") + 1)
        return chr(letter)


################################################################################

def puzzle_01() -> int:
    """
    Each room consists of an encrypted name (lowercase letters separated by
    dashes) followed by a dash, a sector ID, and a checksum in square brackets.

    A room is real (not a decoy) if the checksum is the five most common letters
    in the encrypted name, in order, with ties broken by alphabetization.
    For example:

    -aaaaa-bbb-z-y-x-123[abxyz] is a real room because the most common letters
     are a (5), b (3), and then a tie between x, y, and z, which are listed
     alphabetically.
    -a-b-c-d-e-f-g-h-987[abcde] is a real room because although the letters are
     all tied (1 of each), the first five are listed alphabetically.
    -not-a-real-room-404[oarel] is a real room.
    -totally-real-room-200[decoy] is not.

    Of the real rooms from the list above, the sum of their sector IDs is 1514.

    :return: What is the sum of the sector IDs of the real rooms?
    """

    with open(INPUT_FILE_PATH, "r") as f:
        rooms = [Room(room_line) for room_line in f.readlines()]
        return sum(room.sector_id
                   for room in filter(lambda room: room.is_real, rooms))


################################################################################

def puzzle_02() -> int:
    """
    With all the decoy data out of the way, it's time to decrypt this list and
    get moving.

    The room names are encrypted by a state-of-the-art shift cipher, which is
    nearly unbreakable without the right software. However, the information
    kiosk designers at Easter Bunny HQ were not expecting to deal with a master
    cryptographer like yourself.

    To decrypt a room name, rotate each letter forward through the alphabet a
    number of times equal to the room's sector ID. A becomes B, B becomes C, Z
    becomes A, and so on. Dashes become spaces.

    For example, the real name for qzmt-zixmtkozy-ivhz-343 is "very encrypted
    name".

    :return: What is the sector ID of the room where North Pole objects are
    stored?
    """

    with open(INPUT_FILE_PATH, "r") as f:
        rooms = [Room(room_line) for room_line in f.readlines()]
        return next(filter(
            lambda room:
            GOAL_DECRYPTED_ROOM_NAME == room.decrypted_name, rooms)).sector_id

################################################################################
