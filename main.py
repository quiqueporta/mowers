import sys

from exceptions import (
    InvalidPlateauSize,
    InvalidMowerInitialLocation,
    InvalidMowerMovements
)
from mowers import MowersController


def __read_commands():
    commands = []
    file = open(sys.argv[1], 'r')

    for line in file.readlines():
        commands.extend(line.splitlines())

    return commands


if __name__ == '__main__':

    commands = __read_commands()

    try:
        result = MowersController().execute(commands)
        print('\n'.join(result))
    except InvalidPlateauSize:
        print("The plateau size is invalid")
    except InvalidMowerInitialLocation:
        print("There is an invalid mower initial location")
    except InvalidMowerMovements:
        print("There is an invalid mower movement")
