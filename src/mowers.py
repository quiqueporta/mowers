from typing import List, Tuple, Iterable
from abc import ABC, abstractmethod


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

    def move_forward(self) -> None:
        offset_x, offset_y = self.__heading.forward_offset()
        self.__x += offset_x
        self.__y += offset_y

    def spin_right(self) -> None:
        self.__heading = self.__heading.spin_right()

    def spin_left(self) -> None:
        self.__heading = self.__heading.spin_left()

    def __str__(self) -> str:
        return f"{self.__x} {self.__y} {self.__heading}"


class Mower:

    def __init__(self, initial_position: Position):
        self.__position = initial_position

    def execute(self, movements: str) -> str:
        movements_handlers = {
            "R": self.__position.spin_right,
            "L": self.__position.spin_left,
            "M": self.__position.move_forward,
        }

        for movement in movements:
            movements_handlers[movement]()

        return f"{self.__position}"

    @classmethod
    def deploy_at(cls, position: Position) -> 'Mower':
        return Mower(position)


class MowersController:

    def execute(self, commands: str) -> str:
        commands = Commands(commands)
        result = ""

        for mower_command in commands.next_mower_command():
            mower = Mower.deploy_at(mower_command.initial_position)
            mower_result = mower.execute(mower_command.movement)
            result += f"{mower_result}\n"

        return result


class MowerCommand:

    def __init__(self, initial_position: Position, movement: str):
        self.initial_position = initial_position
        self.movement = movement


class Commands:

    def __init__(self, input: str):
        commands = self.__extract_commands(input)
        self.__plateau_size = commands[0]
        self.__mowers_commands = commands[1:]

    def next_mower_command(self) -> Iterable[MowerCommand]:
        for mower_command in zip(self.__mowers_initial_positions(), self.__mowers_movements()):
            initial_position = mower_command[0]
            movement = mower_command[1]
            yield MowerCommand(initial_position, movement)

    def __mowers_initial_positions(self):
        return [
           self.__create_position_from_string(position) for position in self.__mowers_commands[::2]
        ]

    def __create_position_from_string(self, position: str):
        x, y, heading = position.split(" ")
        return Position(int(x), int(y), Heading.create(heading))

    def __mowers_movements(self):
        return self.__mowers_commands[1::2]

    def __extract_commands(self, commands: str) -> List[str]:
        return commands.split("\n")[:-1]
