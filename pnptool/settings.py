from enum import IntEnum


class Verbosity(IntEnum):
    SILENT = 0
    INFO = 1
    VERBOSE = 2


class Settings:
    verbosity: Verbosity = 1


SETTINGS = Settings()
