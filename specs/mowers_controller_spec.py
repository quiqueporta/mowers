from expects import expect, equal, raise_error
from mamba import before, description, context, it

from exceptions import InvalidPlateauSize, InvalidMowerInitialPosition, InvalidMowerMovements
from mowers import MowersController

with description("Mowers Controller") as self:

    with context("controls a mower"):

        with before.each:
            self.mowers_controller = MowersController()

        with context("rotation"):

            with it("can spin left once"):

                commands = ["5 5", "0 0 N", "L"]

                result = self.mowers_controller.execute(commands)

                expect(result).to(equal(["0 0 W"]))

            with it("can spin left twice"):
                commands = ["5 5", "0 0 N", "LL"]

                result = self.mowers_controller.execute(commands)

                expect(result).to(equal(["0 0 S"]))

            with it("can spin left three times"):
                commands = ["5 5", "0 0 N", "LLL"]

                result = self.mowers_controller.execute(commands)

                expect(result).to(equal(["0 0 E"]))

            with it("can spin left four times"):
                commands = ["5 5", "0 0 N", "LLLL"]

                result = self.mowers_controller.execute(commands)

                expect(result).to(equal(["0 0 N"]))

            with it("can spin right once"):
                commands = ["5 5", "0 0 N", "R"]

                result = self.mowers_controller.execute(commands)

                expect(result).to(equal(["0 0 E"]))

            with it("can spin right twice"):
                commands = ["5 5", "0 0 N", "RR"]

                result = self.mowers_controller.execute(commands)

                expect(result).to(equal(["0 0 S"]))

            with it("can spin right three times"):
                commands = ["5 5", "0 0 N", "RRR"]

                result = self.mowers_controller.execute(commands)

                expect(result).to(equal(["0 0 W"]))

            with it("can spin right four times"):
                commands = ["5 5", "0 0 N", "RRRR"]

                result = self.mowers_controller.execute(commands)

                expect(result).to(equal(["0 0 N"]))

        with context("movement"):

            with it("can move North forward"):
                commands = ["5 5", "0 0 N", "M"]

                result = self.mowers_controller.execute(commands)

                expect(result).to(equal(["0 1 N"]))

            with it("can move East forward"):
                commands = ["5 5", "0 0 E", "M"]

                result = self.mowers_controller.execute(commands)

                expect(result).to(equal(["1 0 E"]))

            with it("can move South forward"):
                commands = ["5 5", "0 1 S", "M"]

                result = self.mowers_controller.execute(commands)

                expect(result).to(equal(["0 0 S"]))

            with it("can move West forward"):
                commands = ["5 5", "1 0 W", "M"]

                result = self.mowers_controller.execute(commands)

                expect(result).to(equal(["0 0 W"]))

    with context("when a mowers tries to move outside the plateau from north"):

        with it("does not execute the move"):

            mowers_controller = MowersController()

            commands = ["1 1", "0 0 N", "MM"]

            result = mowers_controller.execute(commands)

            expected_result = ["0 1 N"]
            expect(result).to(equal(expected_result))

    with context("when a mowers tries to move outside the plateau from east"):

        with it("does not execute the move"):

            mowers_controller = MowersController()

            commands = ["1 1", "0 0 E", "MM"]

            result = mowers_controller.execute(commands)

            expected_result = ["1 0 E"]
            expect(result).to(equal(expected_result))

    with context("when a mowers tries to move outside the plateau from west"):

        with it("does not execute the move"):

            mowers_controller = MowersController()

            commands = ["1 1", "1 0 W", "MM"]

            result = mowers_controller.execute(commands)

            expected_result = ["0 0 W"]
            expect(result).to(equal(expected_result))

    with context("when a mowers tries to move outside the plateau from south"):

        with it("does not execute the move"):

            mowers_controller = MowersController()

            commands = ["1 1", "0 1 S", "MM"]

            result = mowers_controller.execute(commands)

            expected_result = ["0 0 S"]
            expect(result).to(equal(expected_result))

    with it("controls more than one mower"):

        mowers_controller = MowersController()

        commands = ["5 5", "1 2 N", "LMLMLMLMM", "3 3 E", "MMRMMRMRRM"]

        result = mowers_controller.execute(commands)

        expected_result = ["1 3 N", "5 1 E"]
        expect(result).to(equal(expected_result))

    with it("fails when the first command has no correct format"):

        mowers_controller = MowersController()

        commands = ["55", "1 2 N", "LMLMLMLMM"]

        expect(lambda: mowers_controller.execute(commands)).to(raise_error(InvalidPlateauSize))

    with it("fails when the initial position for a mower has no correct format"):

        mowers_controller = MowersController()

        commands = ["5 5", "12N", "LMLMLMLMM"]

        expect(lambda: mowers_controller.execute(commands)).to(raise_error(InvalidMowerInitialPosition))

    with it("fails when the movements for a mower has no correct format"):

        mowers_controller = MowersController()

        commands = ["5 5", "1 2 N", "L ML2 HJMLMM"]

        expect(lambda: mowers_controller.execute(commands)).to(raise_error(InvalidMowerMovements))
