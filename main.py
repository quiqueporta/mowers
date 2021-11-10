import sys

from mowers import MowersController


def __read_commands():
    commands = []
    file = open(sys.argv[1], 'r')

    for line in file.readlines():
        commands.extend(line.splitlines())

    return commands


if __name__ == '__main__':

    commands = __read_commands()
    result = MowersController().execute(commands)

    for line in result:
        print(f"{line}")
