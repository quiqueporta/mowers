import re
from dataclasses import dataclass
from typing import List, Tuple, Iterable
from abc import ABC, abstractmethod

from exceptions import InvalidPlateauSize, InvalidMowerInitialLocation, InvalidMowerMovements


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


@dataclass(frozen=True)
class Coordinate:
    x: int
    y: int

    def __str__(self):
        return f"{self.x} {self.y}"


class Location:

    def __init__(self, coordinate: Coordinate, heading: Heading):
        self.__coordinate = coordinate
        self.__heading = heading

    def move_forward(self) -> None:
        self.__coordinate = self.forward_coordinate()

    def forward_coordinate(self) -> Coordinate:
        offset_x, offset_y = self.__heading.forward_offset()
        return Coordinate(self.__coordinate.x + offset_x, self.__coordinate.y + offset_y)

    def spin_right(self) -> None:
        self.__heading = self.__heading.spin_right()

    def spin_left(self) -> None:
        self.__heading = self.__heading.spin_left()

    def __str__(self) -> str:
        return f"{self.__coordinate} {self.__heading}"


class Plateau:

    def __init__(self, top_right_coordinate: Coordinate):
        self.__bottom_left_coordinate = Coordinate(0, 0)
        self.__top_right_coordinate = top_right_coordinate

    def can_mower_move_to(self, coordinate: Coordinate):
        is_inside_plateau = (
            coordinate.x <= self.__top_right_coordinate.x and
            coordinate.y <= self.__top_right_coordinate.y and
            coordinate.x >= self.__bottom_left_coordinate.x and
            coordinate.y >= self.__bottom_left_coordinate.y
        )

        return is_inside_plateau


class Mower:

    def __init__(self, plateau: Plateau, initial_location: Location):
        self.__plateau = plateau
        self.__location = initial_location

    def execute(self, movements: str) -> str:
        movements_handlers = {
            "R": self.__location.spin_right,
            "L": self.__location.spin_left,
            "M": self.__move_forward,
        }

        for movement in movements:
            movements_handlers[movement]()

        return f"{self.__location}"

    def __move_forward(self):
        if not self.__plateau.can_mower_move_to(self.__location.forward_coordinate()):
            return

        self.__location.move_forward()

    @classmethod
    def deploy_at(cls, location: Location, plateau: Plateau) -> 'Mower':
        return Mower(plateau, location)


class MowersController:

    def execute(self, commands: List[str]) -> List[str]:
        commands = Commands(commands)
        plateau = Plateau(commands.plateau_top_right_coordinate)
        result = []

        for mower_command in commands.next_mower_command():
            mower = Mower.deploy_at(mower_command.initial_location, plateau)
            mower_result = mower.execute(mower_command.movement)
            result.append(mower_result)

        return result


class MowerCommand:

    def __init__(self, initial_location: Location, movement: str):
        self.initial_location = initial_location
        self.movement = movement


class Commands:

    def __init__(self, commands: List[str]):
        self.__commands = commands
        self.__check_commands_format()

    def next_mower_command(self) -> Iterable[MowerCommand]:
        for mower_command in zip(self.__mowers_initial_locations(), self.__mowers_movements()):
            yield MowerCommand(initial_location=mower_command[0], movement=mower_command[1])

    @property
    def plateau_top_right_coordinate(self):
        return Coordinate(int(self.__plateau_size()[0]), int(self.__plateau_size()[2]))

    def __check_commands_format(self):
        plateau_size = self.__plateau_size()
        mowers_initial_locations = self.__mowers_locations()
        mowers_movements = self.__mowers_movements()

        if not re.match(r"^\d \d$", plateau_size):
            raise InvalidPlateauSize()

        if not all(re.match(r"^\d \d [NSEW]+$", location) for location in mowers_initial_locations):
            raise InvalidMowerInitialLocation()

        if not all(re.match(r"^[LMR]+$", movement) for movement in mowers_movements):
            raise InvalidMowerMovements()

    def __plateau_size(self) -> str:
        return self.__commands[0]

    def __mowers_commands(self) -> List[str]:
        return self.__commands[1:]

    def __mowers_locations(self):
        return self.__mowers_commands()[::2]

    def __mowers_movements(self):
        return self.__mowers_commands()[1::2]

    def __mowers_initial_locations(self):
        return [
            self.__create_location_from_string(location)
            for location in self.__mowers_locations()
        ]

    def __create_location_from_string(self, location: str):
        x, y, heading = location.split(" ")

        return Location(Coordinate(int(x), int(y)), Heading.create(heading))
