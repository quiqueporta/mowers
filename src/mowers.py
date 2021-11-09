from typing import List, Tuple
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

    DEFAULT_POSITION = "0 0 N"

    def __init__(self, initial_position: str = DEFAULT_POSITION):
        x, y, heading = initial_position.split(" ")

        self.__position = Position(int(x), int(y), Heading.create(heading))

    def execute(self, commands: str) -> str:
        command_handlers = {
            "R": self.__position.spin_right,
            "L": self.__position.spin_left,
            "M": self.__position.move_forward,
        }

        for command in commands:
            command_handlers[command]()

        return f"{self.__position}"

    @classmethod
    def deploy_at(cls, position: str) -> 'Mower':
        return Mower(position)


class MowersController:

    def execute(self, commands: str) -> str:
        result = ""

        for command in self.__extract_commands(commands):

            if self.__is_mower_initial_position(command):
                mower = Mower.deploy_at(command)
            elif self.__is_mower_movement_command(command):
                mower_result = mower.execute(command)
                result += f"{mower_result}\n"

        return result

    def __extract_commands(self, commands: str) -> List[str]:
        return commands.split("\n")[:-1]

    def __is_mower_initial_position(self, command) -> bool:
        return len(command) == 5 and self.__has_numbers(command)

    def __is_mower_movement_command(self, command) -> bool:
        return not self.__has_numbers(command)

    def __has_numbers(self, command: str) -> bool:
        return any(char.isdigit() for char in command)
