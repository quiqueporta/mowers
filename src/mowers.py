import re
from typing import List, Tuple, Iterable
from abc import ABC, abstractmethod

from exceptions import InvalidPlateauSize, InvalidMowerInitialPosition, InvalidMowerMovements


class Heading(ABC):

    @abstractmethod
    def spin_right(self) -> 'Heading':
        pass

    @abstractmethod
    def spin_left(self) -> 'Heading':
        pass

    @abstractmethod
    def forward_offset(self) -> Tuple[int, int]:
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass

    @staticmethod
    def create(string: str) -> 'Heading':
        HEADINGS = {
            "N": North,
            "S": South,
            "E": East,
            "W": West
        }

        return HEADINGS[string]()


class North(Heading):

    def spin_right(self) -> Heading:
        return East()

    def spin_left(self) -> Heading:
        return West()

    def forward_offset(self) -> Tuple[int, int]:
        return (0, 1)

    def __str__(self) -> str:
        return "N"


class East(Heading):

    def spin_right(self) -> Heading:
        return South()

    def spin_left(self) -> Heading:
        return North()

    def forward_offset(self) -> Tuple[int, int]:
        return (1, 0)

    def __str__(self):
        return "E"


class South(Heading):

    def spin_right(self) -> Heading:
        return West()

    def spin_left(self) -> Heading:
        return East()

    def forward_offset(self) -> Tuple[int, int]:
        return (0, -1)

    def __str__(self):
        return "S"


class West(Heading):

    def spin_right(self) -> Heading:
        return North()

    def spin_left(self) -> Heading:
        return South()

    def forward_offset(self) -> Tuple[int, int]:
        return (-1, 0)

    def __str__(self):
        return "W"


class Position:

    def __init__(self, x: int, y: int, heading: Heading):
        self.__x = x
        self.__y = y
        self.__heading = heading

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    def move_forward(self) -> None:
        offset_x, offset_y = self.__heading.forward_offset()
        self.__x += offset_x
        self.__y += offset_y

    def spin_right(self) -> None:
        self.__heading = self.__heading.spin_right()

    def spin_left(self) -> None:
        self.__heading = self.__heading.spin_left()

    def forward_position(self) -> Tuple[int, int]:
        offset_x, offset_y = self.__heading.forward_offset()
        return (self.__x + offset_x, self.__y + offset_y)

    def __str__(self) -> str:
        return f"{self.__x} {self.__y} {self.__heading}"


class Plateau:

    def __init__(self, max_x: int, max_y: int):
        self.__max_x = max_x
        self.__max_y = max_y

    def can_mower_move_to(self, position: Tuple[int, int]):
        return (
            position[0] <= self.__max_x and
            position[1] <= self.__max_y and
            position[0] >= 0 and
            position[1] >= 0
        )


class Mower:

    def __init__(self, plateau: Plateau, initial_position: Position):
        self.__plateau = plateau
        self.__position = initial_position

    def execute(self, movements: str) -> str:
        movements_handlers = {
            "R": self.__position.spin_right,
            "L": self.__position.spin_left,
            "M": self.__move_forward,
        }

        for movement in movements:
            movements_handlers[movement]()

        return f"{self.__position}"

    def __move_forward(self):
        if not self.__plateau.can_mower_move_to(self.__position.forward_position()):
            return

        self.__position.move_forward()

    @classmethod
    def deploy_at(cls, plateau: Plateau, position: Position) -> 'Mower':
        return Mower(plateau, position)


class MowersController:

    def execute(self, commands: List[str]) -> List[str]:
        commands = Commands(commands)
        plateau = commands.plateau()
        result = []

        for mower_command in commands.next_mower_command():
            mower = Mower.deploy_at(plateau, mower_command.initial_position)
            mower_result = mower.execute(mower_command.movement)
            result.append(mower_result)

        return result


class MowerCommand:

    def __init__(self, initial_position: Position, movement: str):
        self.initial_position = initial_position
        self.movement = movement


class Commands:

    def __init__(self, commands: List[str]):
        self.__commands = commands
        self.__check_commands_format()

    def next_mower_command(self) -> Iterable[MowerCommand]:
        for mower_command in zip(self.__mowers_initial_positions(), self.__mowers_movements()):
            yield MowerCommand(initial_position=mower_command[0], movement=mower_command[1])

    def plateau(self):
        return Plateau(int(self.__plateau_size()[0]), int(self.__plateau_size()[2]))

    def __check_commands_format(self):
        plateau_size = self.__plateau_size()
        mowers_initial_positions = self.__mowers_positions()
        mowers_movements = self.__mowers_movements()

        if not re.match(r"^\d \d$", plateau_size):
            raise InvalidPlateauSize()

        if not all(re.match(r"^\d \d [NSEW]+$", position) for position in mowers_initial_positions):
            raise InvalidMowerInitialPosition()

        if not all(re.match(r"^[LMR]+$", movement) for movement in mowers_movements):
            raise InvalidMowerMovements()

    def __plateau_size(self) -> str:
        return self.__commands[0]

    def __mowers_commands(self) -> List[str]:
        return self.__commands[1:]

    def __mowers_positions(self):
        return self.__mowers_commands()[::2]

    def __mowers_movements(self):
        return self.__mowers_commands()[1::2]

    def __mowers_initial_positions(self):
        return [
            self.__create_position_from_string(position)
            for position in self.__mowers_positions()
        ]

    def __create_position_from_string(self, position: str):
        x, y, heading = position.split(" ")
        return Position(int(x), int(y), Heading.create(heading))
