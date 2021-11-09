from typing import List


class North:

    def spin_right(self):
        return East()

    def spin_left(self):
        return West()

    def __str__(self):
        return "N"


class East:

    def spin_right(self):
        return South()

    def spin_left(self):
        return North()

    def __str__(self):
        return "E"


class South:

    def spin_right(self):
        return West()

    def spin_left(self):
        return East()

    def __str__(self):
        return "S"


class West:

    def spin_right(self):
        return North()

    def spin_left(self):
        return South()

    def __str__(self):
        return "W"


class Position:

    def __init__(self, x: int, y: int, heading):
        self.__x = x
        self.__y = y
        self.__heading = heading

    def move_forward(self):
        movements = {
            'N': self.__move_up,
            'S': self.__move_down,
            'W': self.__move_left,
            'E': self.__move_right,
        }

        movements[str(self.__heading)]()

    def spin_right(self):
        self.__heading = self.__heading.spin_right()

    def spin_left(self):
        self.__heading = self.__heading.spin_left()

    def __move_up(self):
        self.__y += 1

    def __move_down(self):
        self.__y -= 1

    def __move_left(self):
        self.__x -= 1

    def __move_right(self):
        self.__x += 1

    def __str__(self):
        return f"{self.__x} {self.__y} {self.__heading}"


class Mower:

    ORIENTATIONS = {
        "N": North,
        "S": South,
        "E": East,
        "W": West
    }

    def __init__(self, initial_position: str = "0 0 N"):
        x, y, orientation = initial_position.split(" ")

        self.__position = Position(int(x), int(y), self.ORIENTATIONS[orientation]())

    def execute(self, commands: str):

        for command in commands:
            if command == "R":
                self.__position.spin_right()
            elif command == "L":
                self.__position.spin_left()
            elif command == "M":
                self.__position.move_forward()

        return f"{self.__position}"

    @classmethod
    def deploy_at(cls, position):
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
        return len(command) == 5

    def __is_mower_movement_command(self, command) -> bool:
        return len(command) > 5
