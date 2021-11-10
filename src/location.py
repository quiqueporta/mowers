from dataclasses import dataclass

from heading import Heading


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
