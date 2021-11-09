class North:

    def rotate_right(self):
        return East()

    def rotate_left(self):
        return West()

    def __str__(self):
        return "N"


class East:

    def rotate_right(self):
        return South()

    def rotate_left(self):
        return North()

    def __str__(self):
        return "E"


class South:

    def rotate_right(self):
        return West()

    def rotate_left(self):
        return East()

    def __str__(self):
        return "S"


class West:

    def rotate_right(self):
        return North()

    def rotate_left(self):
        return South()

    def __str__(self):
        return "W"


class Mower:

    def __init__(self):
        self.__current_orientation = North()

    def execute(self, commands: str):

        for command in commands:
            if command == "R":
                self.__current_orientation = self.__current_orientation.rotate_right()
            elif command == "L":
                self.__current_orientation = self.__current_orientation.rotate_left()

        return f"0 0 {self.__current_orientation}"
