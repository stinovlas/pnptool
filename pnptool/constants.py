from typing import NamedTuple


class Offset(NamedTuple):
    top: int
    right: int
    bottom: int
    left: int


# PocketMod constants
# POCKETMOD_OFFSET = (47, 37, 37, 34)  # top, right, bottom, left
POCKETMOD_OFFSET = Offset(top=47, right=37, bottom=0, left=34)
POCKETMOD_ROWS = 1
POCKETMOD_COLUMNS = 4
POCKETMOD_PAGES_SEQ = (7, 0, 1, 2, 3, 4, 5, 6)
POCKETMOD_PDF_PAGES = (0,)
